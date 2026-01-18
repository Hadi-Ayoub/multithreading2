Ce projet implémente une architecture de calcul distribué permettant de résoudre des opérations matricielles lourdes (Ax=B). Il compare les performances entre des workers (Minions) écrits en **Python (NumPy)** et en **C++ (Eigen)**, communiquant via une interface HTTP.


## Architecture du Projet

Le système final repose sur une architecture modulaire en 4 composants :

- **Manager** : Serveur central qui stocke les tâches et résultats via `multiprocessing.managers`.
- **Boss** : Client qui génère les tâches (matrices aléatoires).
- **Proxy** : Serveur HTTP qui traduit les objets Python en JSON pour le monde extérieur.
- **Workers** : Agents de calcul (Python ou C++).

---

## Analyse des Performances (Benchmarks)

Les tests comparent le temps de calcul pur (en moyenne) pour résoudre un système linéaire selon la taille de la matrice N×N sans intégrer le temps des traitements I/O.

| Taille Matrice (N) | Python (NumPy) | C++ (Eigen Release) | Vainqueur |
|--------------------|----------------|---------------------|------------------------|
| N = 100 | ~0.0008s | ~0.0001s | C++ (8x plus vite) |
| N = 1000 | ~0.0150s | ~0.0200s |  numpy légèrement supérieur |
| N = 5000 | ~0.5300s | ~1.4000s |  Python (NumPy) |

###  Conclusions Techniques

1. **Le Mur du JSON (I/O Bottleneck)** :
   - Pour N=5000, une seule tâche pèse environ 500 Mo une fois convertie en texte JSON (contre 200 Mo en binaire).
   - Le Worker C++ passe 99% de son temps à télécharger et parser ce texte, et moins de 1% à faire le calcul mathématique.


2. **Calcul Pur & Multithreading** :
   - NumPy utilise des bibliothèques (BLAS/MKL) qui parallélisent automatiquement le calcul sur tous les cœurs du CPU.
   - C++ (Eigen) est exécuté ici en mono-thread. Bien que très rapide intrinsèquement , il est désavantagé sur les très grosses matrices.

3. **Latence vs Débit** :
   - Sur de petites tâches (N=100), l'architecture HTTP/C++ est pénalisée par la latence réseau (Handshake TCP, headers HTTP). Python (local) est immédiat grâce à la mémoire partagée.

---

## Pré-requis et Installation

### Outils nécessaires

- **Python** : 3.10 ou supérieur
- **C++** : CMake (3.14+) et un compilateur compatible C++17.
- **uv** : Gestionnaire de package Python rapide.

### Installation

1. **Installer uv**  :
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Installer les dépendances Python** :
   ```bash
   uv sync
   ```

3. **Compiler le client C++** :

    **Attention** : La compilation en mode Release est obligatoire pour les performances (Active SIMD/AVX).

   ```bash
   cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
   cmake --build build
   ```

---

##  Utilisation

### Lancer le système complet

1. **Démarrer le Manager** (serveur de queues) :
   ```bash
   uv run python manager.py
   ```

2. **Démarrer le Proxy HTTP** (passerelle pour C++) :
   ```bash
   uv run python proxy.py
   ```

3. **Lancer les Workers** :

   - Worker Python :
     ```bash
     uv run python minion_python.py
     ```

   - Worker C++ :
     ```bash
     ./build/minion_cpp
     ```

4. **Exécuter le Boss** (client générateur de tâches) :
   ```bash
   uv run python boss.py
   ```

---
