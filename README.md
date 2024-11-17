# Emil-the-Unicorne 🦄
An intelligent Discord bot using local language patterns to naturally analyze and participate in conversations. Able to understand context, manage ongoing discussions and generate appropriate responses for you Discord Account with the channel of your choice.
# Discord AI Conversation Bot

Un bot Discord intelligent capable d'analyser et de participer naturellement aux conversations en utilisant des modèles de langage locaux.

## 🌟 Caractéristiques

- Analyse automatique de l'état des conversations
- Réponses naturelles et contextuelles
- Hébergement local des modèles d'IA
- Personnalisation facile du comportement du bot
- Gestion intelligente des fils de discussion

## 🛠️ Prérequis

- Python 3.8+
- Un modèle de langage local compatible (ex: LLama, Mistral...)
- Une application Discord enregistrée
- Les bibliothèques Python requises (voir `requirements.txt`)

## 📦 Installation

```bash
# Cloner le repository
git clone https://github.com/VotreUsername/discord-ai-bot

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos configurations
```

## ⚙️ Configuration

1. Créez une application sur le [Portail Développeur Discord](https://discord.com/developers/applications)
2. Configurez le fichier `.env` :
```env
DISCORD_TOKEN=votre_token_discord
MODEL_PATH=chemin_vers_votre_modele_local
```

## 🚀 Utilisation

1. Lancez le bot :
```bash
python main.py
```

2. Le bot analysera automatiquement les conversations et répondra de manière appropriée

## 📝 Fonctionnement

Le bot utilise deux systèmes de prompts principaux :

### Analyseur de Conversation
- Évalue si une conversation est en cours ou terminée
- Prend en compte le contexte et la cohérence
- Gère les questions en attente et les interactions incomplètes

### Générateur de Réponses
- Produit des réponses naturelles et contextuelles
- Adapte le ton et le style selon la conversation
- Maintient une personnalité cohérente

## 🔧 Personnalisation

Vous pouvez personnaliser le comportement du bot en modifiant les prompts dans `config/prompts/` :
- `analyzer_prompt.txt` : Règles d'analyse des conversations
- `response_prompt.txt` : Configuration de la personnalité et du style de réponse

## 📈 Exemples d'Utilisation

```python
# Exemple d'analyse de conversation
conversation = [
    {"author": "User1", "content": "Salut !"},
    {"author": "Bot", "content": "Hey, comment ça va ?"},
    {"author": "User1", "content": "Super et toi ?"}
]
status = analyzer.analyze(conversation)
# Résultat : "non (question en attente)"

# Exemple de génération de réponse
response = generator.generate(conversation)
# Résultat : "Nickel ! Tu fais quoi de beau ?"
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add: Amazing Feature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 🙏 Remerciements

- Discord.py pour leur excellente API
- La communauté des modèles de langage open source
