KILL666
<img width="1000" height="1000" alt="m1000x1000" src="https://github.com/user-attachments/assets/b4cb39cc-7311-4e2c-88e9-e410c39b6765" />

> **Créé par :** `hackers_tchad`  
> **Version :** `v666.0 - TCHAD DARK EDITION`  
> **Type :** Chat privé LAN / réseau privé avec vidéo, voix, transfert de fichiers

---

##  DESCRIPTION

**KILL666** est une interface Tkinter/CustomTkinter avancée de communication privée :

-  **Chat texte en direct** visible par tous les utilisateurs connectés
-  **Vidéo en direct**
-  **Vocal en direct** entre utilisateurs (push-to-talk ou continu)
-  **Transfert de fichiers** chiffrés AES-256-GCM
-  **Profil utilisateur** (pseudo, avatar, statut, bio) lors de la connexion
-  **Réseau privé** : connexion via IP/port personnalisé
-  **Mode hôte/client** : l'un héberge, les autres rejoignent

---

##  INSTALLATION

```bash
git clone https://github.com/hackerstchad/KILL666.git
cd kill666
pip install -r requirements.txt
```

### Prérequis audio (Windows/Linux)
```bash
# Windows
pip install pyaudio

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
```

---

## 🚀 UTILISATION

### Lancer KILL666
```bash
python kill666.py
```

### Créer un salon (Hôte)
1. Entrez votre pseudo
2. Remplissez votre profil
3. Cliquez sur **"Create Private Room"**
4. Partagez l'IP et le port affichés

### Rejoindre un salon (Client)
1. Entrez votre pseudo
2. Remplissez votre profil
3. Renseignez l'IP et le port de l'hôte
4. Cliquez sur **"Join Private Room"**

---

##  Contrôles

| Action | Description |
|--------|-------------|
| `T` | Activer/désactiver le micro (push-to-talk) |
| `C` | Activer/désactiver la caméra |
| `F` | Envoyer un fichier |
| `M` | Changer de thème couleur |
| `L` | Afficher les logs réseau |
| `P` | Ouvrir le panel profil |
| `ESC` | Quitter |

---

##  SÉCURITÉ

- Chiffrement AES-256-GCM pour les messages privés et fichiers
- Réseau privé uniquement (pas de serveur public)
- Logs locaux chiffrés
- Authentification par mot de passe de salon optionnelle

---

---

##  Développeur

```text
hackers_tchad
Tchad · Cyber · Dark Comms
```

---

##  Licence

MIT — CYBER - CRIME

