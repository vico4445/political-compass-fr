"""
Projections des votes dans un espace 2D
Compare LDA, PCA, t-SNE et UMAP
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
import umap
import json


class VoteProjector:
    """Projecteur de votes en 2D"""

    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.results_dir = self.data_dir / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Configuration des plots
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

    def load_data(self):
        """Charge la matrice de votes et les métadonnées"""
        print(f"\n{'='*60}")
        print("CHARGEMENT DES DONNÉES")
        print(f"{'='*60}")

        # Charger la matrice complète
        vote_matrix_path = self.processed_dir / "vote_matrix.csv"
        df = pd.read_csv(vote_matrix_path)

        print(f"✓ Matrice chargée: {df.shape}")

        # Séparer les métadonnées et les données de vote
        meta_cols = ['numero', 'titre', 'date', 'thematique']
        vote_cols = [col for col in df.columns if col not in meta_cols]

        X = df[vote_cols].values
        metadata = df[meta_cols]

        print(f"  - Données de vote: {X.shape}")
        print(f"  - Groupes parlementaires: {len(vote_cols)}")
        print(f"  - Métadonnées: {metadata.shape[1]} colonnes")

        return X, metadata, vote_cols

    def apply_pca(self, X, n_components=2):
        """Applique PCA (Principal Component Analysis)"""
        print(f"\n{'='*60}")
        print("PCA - PRINCIPAL COMPONENT ANALYSIS")
        print(f"{'='*60}")

        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X)

        print(f"✓ PCA appliquée")
        print(f"  - Variance expliquée par PC1: {pca.explained_variance_ratio_[0]:.3f}")
        print(f"  - Variance expliquée par PC2: {pca.explained_variance_ratio_[1]:.3f}")
        print(f"  - Variance totale expliquée: {pca.explained_variance_ratio_.sum():.3f}")

        return X_pca, pca

    def apply_lda(self, X, labels, n_components=2):
        """Applique LDA (Linear Discriminant Analysis)"""
        print(f"\n{'='*60}")
        print("LDA - LINEAR DISCRIMINANT ANALYSIS")
        print(f"{'='*60}")

        # LDA nécessite des labels de classe
        # On va utiliser les thématiques comme classes
        n_unique_labels = len(np.unique(labels))
        n_components = min(n_components, n_unique_labels - 1)

        print(f"  - Nombre de classes (thématiques): {n_unique_labels}")
        print(f"  - Composantes LDA: {n_components}")

        lda = LDA(n_components=n_components)
        X_lda = lda.fit_transform(X, labels)

        print(f"✓ LDA appliquée")
        print(f"  - Variance expliquée par LD1: {lda.explained_variance_ratio_[0]:.3f}")
        if n_components > 1:
            print(f"  - Variance expliquée par LD2: {lda.explained_variance_ratio_[1]:.3f}")

        return X_lda, lda

    def apply_tsne(self, X, perplexity=30, random_state=42):
        """Applique t-SNE (t-Distributed Stochastic Neighbor Embedding)"""
        print(f"\n{'='*60}")
        print("t-SNE - STOCHASTIC NEIGHBOR EMBEDDING")
        print(f"{'='*60}")

        # Ajuster la perplexité si nécessaire
        n_samples = X.shape[0]
        perplexity = min(perplexity, n_samples - 1)

        print(f"  - Perplexité: {perplexity}")
        print(f"  - État aléatoire: {random_state}")

        tsne = TSNE(n_components=2, perplexity=perplexity, random_state=random_state, max_iter=1000)
        X_tsne = tsne.fit_transform(X)

        print(f"✓ t-SNE appliquée")
        print(f"  - KL divergence: {tsne.kl_divergence_:.3f}")

        return X_tsne, tsne

    def apply_umap(self, X, n_neighbors=15, min_dist=0.1, random_state=42):
        """Applique UMAP (Uniform Manifold Approximation and Projection)"""
        print(f"\n{'='*60}")
        print("UMAP - MANIFOLD APPROXIMATION")
        print(f"{'='*60}")

        # Ajuster n_neighbors si nécessaire
        n_samples = X.shape[0]
        n_neighbors = min(n_neighbors, n_samples - 1)

        print(f"  - Nombre de voisins: {n_neighbors}")
        print(f"  - Distance minimale: {min_dist}")
        print(f"  - État aléatoire: {random_state}")

        umap_model = umap.UMAP(n_components=2, n_neighbors=n_neighbors,
                               min_dist=min_dist, random_state=random_state)
        X_umap = umap_model.fit_transform(X)

        print(f"✓ UMAP appliquée")

        return X_umap, umap_model

    def plot_projection(self, X_proj, metadata, title, filename, method_name):
        """
        Crée une visualisation de la projection

        Args:
            X_proj: Coordonnées 2D projetées
            metadata: DataFrame avec métadonnées (thematique, titre, etc.)
            title: Titre du plot
            filename: Nom du fichier de sortie
            method_name: Nom de la méthode (pour les labels d'axes)
        """
        fig, ax = plt.subplots(figsize=(14, 10))

        # Créer un mapping couleur pour les thématiques
        themes = metadata['thematique'].unique()
        colors = sns.color_palette("husl", len(themes))
        theme_to_color = {theme: colors[i] for i, theme in enumerate(themes)}

        # Plot des points par thématique
        for theme in themes:
            mask = metadata['thematique'] == theme
            ax.scatter(X_proj[mask, 0], X_proj[mask, 1],
                      label=theme, alpha=0.7, s=100,
                      color=theme_to_color[theme], edgecolors='black', linewidth=0.5)

        # Configuration
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(f'{method_name} Composante 1', fontsize=12)
        ax.set_ylabel(f'{method_name} Composante 2', fontsize=12)
        ax.legend(title='Thématique', loc='best', framealpha=0.9, fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Sauvegarder
        output_path = self.results_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Visualisation sauvegardée: {output_path}")

        plt.close()

    def plot_comparison(self, projections_dict, metadata):
        """
        Crée une figure de comparaison des 4 méthodes

        Args:
            projections_dict: Dict avec les projections {method_name: X_proj}
            metadata: DataFrame avec métadonnées
        """
        print(f"\n{'='*60}")
        print("CRÉATION DE LA VISUALISATION COMPARATIVE")
        print(f"{'='*60}")

        fig, axes = plt.subplots(2, 2, figsize=(18, 16))
        axes = axes.flatten()

        # Créer un mapping couleur pour les thématiques
        themes = metadata['thematique'].unique()
        colors = sns.color_palette("husl", len(themes))
        theme_to_color = {theme: colors[i] for i, theme in enumerate(themes)}

        method_names = ['PCA', 'LDA', 't-SNE', 'UMAP']

        for idx, (method, X_proj) in enumerate(projections_dict.items()):
            ax = axes[idx]

            # Plot des points par thématique
            for theme in themes:
                mask = metadata['thematique'] == theme
                ax.scatter(X_proj[mask, 0], X_proj[mask, 1],
                          label=theme, alpha=0.7, s=80,
                          color=theme_to_color[theme], edgecolors='black', linewidth=0.5)

            ax.set_title(f'{method_names[idx]} Projection', fontsize=14, fontweight='bold')
            ax.set_xlabel(f'Composante 1', fontsize=11)
            ax.set_ylabel(f'Composante 2', fontsize=11)
            ax.grid(True, alpha=0.3)

            if idx == 0:
                ax.legend(title='Thématique', loc='best', framealpha=0.9, fontsize=8)

        plt.suptitle('Comparaison des méthodes de projection', fontsize=18, fontweight='bold', y=0.995)
        plt.tight_layout()

        # Sauvegarder
        output_path = self.results_dir / "comparison_all_methods.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Comparaison sauvegardée: {output_path}")

        plt.close()

    def save_projections(self, projections_dict, metadata):
        """Sauvegarde les coordonnées des projections"""
        print(f"\n{'='*60}")
        print("SAUVEGARDE DES PROJECTIONS")
        print(f"{'='*60}")

        for method, X_proj in projections_dict.items():
            # Créer un DataFrame avec métadonnées et coordonnées
            df = metadata.copy()
            df[f'{method}_x'] = X_proj[:, 0]
            df[f'{method}_y'] = X_proj[:, 1]

            # Sauvegarder
            output_path = self.processed_dir / f"projection_{method.lower()}.csv"
            df.to_csv(output_path, index=False)
            print(f"  ✓ {method}: {output_path}")


def main():
    """Fonction principale"""
    print(f"\n{'#'*60}")
    print("# PROJECTIONS 2D - POLITICAL COMPASS FR")
    print(f"{'#'*60}\n")

    projector = VoteProjector()

    # Charger les données
    X, metadata, vote_cols = projector.load_data()

    # Appliquer les 4 méthodes
    projections = {}

    # 1. PCA
    X_pca, pca_model = projector.apply_pca(X)
    projections['PCA'] = X_pca
    projector.plot_projection(X_pca, metadata,
                             "PCA - Projection des votes parlementaires",
                             "projection_pca.png", "PCA")

    # 2. LDA (utilise les thématiques comme labels)
    labels = metadata['thematique'].values
    X_lda, lda_model = projector.apply_lda(X, labels)
    projections['LDA'] = X_lda
    projector.plot_projection(X_lda, metadata,
                             "LDA - Séparation par thématiques",
                             "projection_lda.png", "LDA")

    # 3. t-SNE
    X_tsne, tsne_model = projector.apply_tsne(X)
    projections['t-SNE'] = X_tsne
    projector.plot_projection(X_tsne, metadata,
                             "t-SNE - Structure locale des votes",
                             "projection_tsne.png", "t-SNE")

    # 4. UMAP
    X_umap, umap_model = projector.apply_umap(X)
    projections['UMAP'] = X_umap
    projector.plot_projection(X_umap, metadata,
                             "UMAP - Topologie des votes",
                             "projection_umap.png", "UMAP")

    # Créer la comparaison
    projector.plot_comparison(projections, metadata)

    # Sauvegarder les projections
    projector.save_projections(projections, metadata)

    print(f"\n{'='*60}")
    print("PROJECTIONS TERMINÉES!")
    print(f"{'='*60}\n")
    print("Résultats disponibles dans:")
    print(f"  - {projector.results_dir}")
    print("\nFichiers générés:")
    print("  - projection_pca.png")
    print("  - projection_lda.png")
    print("  - projection_tsne.png")
    print("  - projection_umap.png")
    print("  - comparison_all_methods.png")


if __name__ == "__main__":
    main()
