import requests
from datetime import datetime
from openai import OpenAI
import re
import time
import threading
#A REMPLIRE
TOKEN = "DZAFZfz5241f6ezd4fds34fdsFAZFSQ" #EXEMPLE
CHANNEL_ID = 126574815314561534 #EXEMPLE

USERNAME = (requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': TOKEN}).json()['global_name'],requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': TOKEN}).json()['username'])
links = ""

header = {
    'authorization': TOKEN
}

def split_text_with_punctuation(text):
    # Utilise une expression régulière pour trouver les phrases
    pattern = r'([^.!?]*[.!?])'
    sentences = re.findall(pattern, text)
    
    # Supprime les espaces en trop après les ponctuations et avant la prochaine phrase
    cleaned_sentences = [re.sub(r'\s*\.\s*', '.', s) for s in sentences]
    
    # Exclut les points (.) du résultat final
    result = [sentence.strip('.') for sentence in cleaned_sentences if sentence.strip('.').strip()]
    
    return result

def detect_and_remove_link(text):
    pattern = r'https:\/\/tenor\.com[^ ]+'
    links = re.findall(pattern, text)
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text, links

class TypingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_flag = threading.Event()

    def run(self):
        while not self.stop_flag.is_set():
            try:
                url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/typing'
                requests.post(url, headers=header)
                time.sleep(8)
            except:
                break

    def stop(self):
        self.stop_flag.set()

def recup_mess(limit):
    Discus = ""
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit={limit}'
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        messages = response.json()
        messages.reverse()

        for message in messages:
            author_username = message.get('author', {}).get('global_name', 'Unknown')
            Discus = Discus + f"{author_username}: {message['content']}" +"\n"
            
            if 'attachments' in message and len(message['attachments']) > 0:
                attachment = message['attachments'][0]
                content_type_key = 'content_type' if 'content_type' in attachment else 'contentType'
                
                if attachment[content_type_key].startswith('image/'):
                    image_url = attachment['url']
                    image_name = f"{attachment['id']}.{attachment['filename'].split('.')[-1]}"
                    with open(image_name, 'wb') as file:
                        response_img = requests.get(image_url)
                        file.write(response_img.content)
                    Discus = Discus + f"Image : {image_name}" +"\n"
    else:
        Discus = Discus + f"Erreur : {response.status_code}" +"\n"
    return(Discus)

def Finishing():
    print("Analyse de la situation de la conversation en cours ...")
    strict_content = f"""
    Tu es un analyseur binaire de conversations Discord. Ta tâche est d'évaluer si une interaction est terminée.
    
    PRIORITE ABSOLUE AU QUESTIONS posé AUTRE QUE TOI ({USERNAME[0]}) sans reponse de ta part -> non
    
    RÈGLES FONDAMENTALES :

    - Réponds UNIQUEMENT et TOUJOURS par "oui" ou "non (raison "indique rapidement pourquoi")"
    - Analyse en priorité les messages les plus récents
    - Priorité ABSOLU SUR LES QUESTIONS PAS DE TOI sans réponse
    - Si une question autre que TOI ({USERNAME[0]}), as été posé sans réponse de Toi ({USERNAME[0]}), Répond Non
    - Si {USERNAME[0]} commence à parler tout seul, ou {USERNAME[0]} as envoyer plus de 4 messages d'affilé. Répond Oui

    RÉPONSE "OUI" SI :

    - Conversation naturellement conclue
    - + 4 message d'affilé est de toi
    - Plus de 5 minutes sans nouveau message
    - Message de conclusion clair (merci, au revoir, etc.)
    - REPOND UNIQUEMENT OUI

    RÉPONSE "NON (raison)" SI :

    - Question d'un autre utilisateur sans réponse -> "non (question en attente)"
    - Conflit actif -> "non (conflit sur "indique le sujet")"
    - Discussion démarre -> "non (début discussion)"
    - Nouvelle thématique -> "non (nouveau sujet sur "indique le sujet")"
    - Tension visible -> "non (tension visible par rapport "indique le sujet")"
    - Attente de réaction -> "non (attente réponse par rapport a "indique la question")"
    

    Considère la conversation comme terminée si :

    - plus 4 message d'affilé est que de toi
    - Le dernier message est une réponse complète
    - Il y a une conclusion claire
    """

    try:
        client = OpenAI(base_url="", api_key="")
        completion = client.chat.completions.create(
            model="",
            messages=[
                {"role": "system", "content": strict_content},
                {"role": "user", "content": recup_mess(5)}
            ],
            temperature=0.4,
        )

        cont = completion.choices[0].message.content
        print(cont)
        print("Analyse de la situation de la conversation terminer!")
        return(cont)
    except Exception as e:
        print(f"Erreur lors de la génération du message: {e}")

def gen_mess(discuss_contexte,Discus):
    print("Generation du Message en cours ...")
    Discus = discuss_contexte +"\n"+ Discus
    complex_content = f"""
    CONTEXTE :

    Tu es {USERNAME[0]} et participes à une conversation Discord
    Analyse le contexte et le ton de la discussion (aide en haut de la conversation)
    Ne mentionne jamais ton nom d'utilisateur à gauche de ta réponse

    PERSONNALITÉ ADAPTATIVE :

    - Style décontracté et direct
    - Utilisation d'abréviation si approprié
    - Ton franc, possiblement sarcastique
    - Expression subtile et naturelle des émotions

    RÈGLES DE RÉPONSE :

    -Fournis UNIQUEMENT le contenu du message, sans préfixe utilisateur
    - 1-2 phrases MAXIMUM
    - Émojis format :texte: (usage rare)
    - Reste dans le sujet
    - Adapte le langage au contexte
    - Pas d'insertion d'image.

    RESTRICTIONS ADAPTATIVE :

    - Messages adapté, courts et directs
    - Pas de formules de politesse excessives
    - Évite le langage soutenu
    - Jamais de référence à l'IA
    - Pas d'explications techniques
    - Maximum 2 phrases, PAS PLUS

    STYLE ADAPTATIVE :

    - Ponctuation adapté
    - MAJUSCULES pour emphase si nécessaire
    - Onomatopées possibles (mdrr, hein, bah, ui, nn, mtn, pk, vrm)
    - Garde le style de {USERNAME[0]}
    """

    try:
        client = OpenAI(base_url="", api_key="")
        completion = client.chat.completions.create(
            model="",
            messages=[
                {"role": "system", "content": complex_content},
                {"role": "user", "content": Discus}
            ],
            temperature=2,
        )

        cont = completion.choices[0].message.content
        cont, links = detect_and_remove_link(cont)

        cont = split_text_with_punctuation(cont)
        print(cont)
        print("Message Generer !")
        for i in range(len(cont)):
            # Créer et démarrer le thread de typing
            typing_thread = TypingThread()
            typing_thread.start()
            #Attend en fonction de la longueur du message pour envoyer le message
            time.sleep(len(cont[i])/5) #4 car c'est la vitesse moyenne d'un humain (moi c'est /5)
            requests.post(f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages',data={'content': cont[i]}, headers=header)
            # Arrêter le thread de typing
            typing_thread.stop()
            typing_thread.join()
        if links != "":
            requests.post(f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages',data={'content': links}, headers=header)
            
    except Exception as e:
        print(f"Erreur lors de la génération du message: {e}")
        # Arrêter le thread de typing en cas d'erreur
        typing_thread.stop()
        typing_thread.join()
    verif_situation()
    
def verif_situation():
    finish = Finishing()
    if finish.startswith("oui"):
        return(True)
    elif finish.startswith("non"):
        gen_mess(finish[len("non"):].strip(),recup_mess(20))
        return(True)
    else:
        return(False)


while True:
    temp = recup_mess(1)
    parts = temp.split(":")
    if parts[0] != USERNAME[0]:
        print(verif_situation())