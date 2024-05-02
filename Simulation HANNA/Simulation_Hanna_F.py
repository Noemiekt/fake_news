import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def run_simulation(followers, activity_rates, credibility_rates, engagement_rates, num_influencers, total_users, influencer_usernames=None, recovery_time=10000, velocity=2):
    # Initialisation de Pygame
    pg.init()

    # Configuration de la fenêtre
    width, height = 1000, 750
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Simulation de la Propagation de Désinformation")

    # Définition des couleurs par état
    colors = {"S": (0, 0, 255), "I": (255, 0, 0), "R": (0, 255, 0)}

    # Pour stocker le nombre d'individus dans chaque état à chaque itération
    data = {"S": [], "I": [], "R": []}

    population = []

    class Person:
        def __init__(self, username, influencer=False, followers=0, activity_rate=0.0, credibility_rate=1.0, engagement_rate=1.0, following=None):
            self.username = username
            self.followers = followers
            self.following = following if following else []
            self.influencer = influencer
            self.activity_rate = activity_rate
            self.credibility_rate = credibility_rate
            self.engagement_rate = engagement_rate
            self.status = 'I' if influencer else 'S'
            self.position = np.random.rand(2) * np.array([width, height])
            self.velocity = np.random.randn(2) * velocity
            self.infection_time = pg.time.get_ticks() if influencer else None
            self.infected_by = self if influencer else None

        def move(self):
            self.position += self.velocity
            self.position[0] = max(0, min(self.position[0], width))
            self.position[1] = max(0, min(self.position[1], height))

        def update_status(self):
            if self.status == 'I' and pg.time.get_ticks() - self.infection_time > recovery_time:
                self.status = 'R'

        def draw(self):
            color = colors[self.status]
            pg.draw.circle(screen, color, self.position.astype(int), 5)

    # Création de la population
    population = [Person(username=f"user{i+1}", influencer=False) for i in range(total_users - num_influencers)]

    # Détermination des noms pour les influenceurs
    if influencer_usernames is None:
        influencer_usernames = [f"influencer{i+1}" for i in range(num_influencers)]


    for i in range(num_influencers):
        username = influencer_usernames[i] if influencer_usernames else f"influencer{i+1}"
        influencer = Person(username=username, influencer=True, followers=followers[i], activity_rate=activity_rates[i], credibility_rate=credibility_rates[i], engagement_rate=engagement_rates[i])
        population.append(influencer)

    # Initialisation du contrôle du temps
    start_time = pg.time.get_ticks()
    simulation_duration = 25000  # Durée en millisecondes (35 secondes)


    # Simulation principale
    clock = pg.time.Clock()
    running = True
    while running:
        current_time = pg.time.get_ticks()
        if current_time - start_time >= simulation_duration:
            running = False  # Arrête la simulation après 35 secondes

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fond blanc

        credibility_weight = 0.50
        activity_weight = 0.25
        engagement_weight = 0.25

        for person in population:
            person.move()
            person.update_status()
            person.draw()
            if person.status == 'I':
                for other in population:
                    if np.linalg.norm(person.position - other.position) < 10 and other.status == 'S':

                        # Calculer la probabilité d'infection basée sur la crédibilité, le taux d'activité et le taux d'engagement
                        infection_probability = credibility_weight * person.credibility_rate + activity_weight * person.activity_rate + engagement_weight * person.engagement_rate
                        infection_chance = infection_probability * (person.credibility_rate + person.activity_rate + person.engagement_rate)

                        # Augmenter la probabilité si 'other' suit 'person'
                        if person.username in other.following:
                            follow_influence_factor = 2
                            infection_chance *= follow_influence_factor  # follow_influence_factor > 1
                    
                        # Si follow_influence_factor = 1, suivre un influenceur n'a aucun effet sur la probabilité d'être influencé.
                        # Si follow_influence_factor = 2, un follower est deux fois plus susceptible d'être influencé par cet influenceur que quelqu'un qui ne le suit pas.
                        # Si follow_influence_factor = 0.5, suivre un influenceur réduit en fait la probabilité d'être influencé (ce qui pourrait être contre-intuitif dans la plupart des cas).

                        if person.influencer:
                            infection_chance *= person.activity_rate
                        if np.random.rand() < infection_chance:
                            other.status = 'I'
                            other.infection_time = pg.time.get_ticks()
                            other.infected_by = person.infected_by
        
        # Recalculez les infections après la fin de la simulation
        influencer_data = [
            {
                'username': person.username,
                'followers': person.followers,
                'activity_rate': person.activity_rate,
                'credibility_rate': person.credibility_rate,
                'engagement_rate': person.engagement_rate,
                'infections': sum(1 for p in population if p.infected_by == person and p != person)
            }
            for person in population if person.influencer
        ]

        pg.display.flip()
        clock.tick(30)

        # Compter et enregistrer le nombre d'individus dans chaque état
        counts = {"S": 0, "I": 0, "R": 0}
        for person in population:
            counts[person.status] += 1
        for status in ["S", "I", "R"]:
            data[status].append(counts[status])

    pg.quit()

    return data, population, influencer_data  # Renvoie les données de simulation pour analyse



def prepare_sir_data(data):
    """ Prépare les données SIR pour la visualisation """
    # Création d'un DataFrame à partir des données SIR
    df_sir = pd.DataFrame(data)
    return df_sir


def automate_simulations1(params_list):
    for i, params in enumerate(params_list):
        data, population, influencer_data = run_simulation(*params)

        # Préparer les données SIR
        data_sir = prepare_sir_data(data)

        # Pour chaque simulation, préparez les données pour l'enregistrement
        influencer_results = []
        for influencer in influencer_data:
            influencer_results.append({
                'influencer': influencer['username'],  # Utilisez la clé 'username'
                'followers_count': influencer['followers'],
                'activity_rates': influencer['activity_rate'],
                'credibility_rates': influencer['credibility_rate'],
                'engagement_rates': influencer['engagement_rate'],
                'infections': influencer['infections']
            })

        # Création d'un DataFrame pour les données des influenceurs
        df = pd.DataFrame(influencer_results)
        
        # Enregistrement des résultats dans un fichier CSV, un fichier par simulation
        file_name = f"Scénario_{i+1}.csv"
        df.to_csv(file_name, index=False)
        print(f"Results for scenario {i+1} saved to {file_name}")

        # Visualiser les résultats pour ce scénario
        display_results1(data_sir, influencer_data)
    

def display_results1(data_sir, influencer_data):
    # Conversion de la liste de dictionnaires en DataFrame
    df = pd.DataFrame(influencer_data)
    df['Influenceur'] = ['Influenceur' + str(i+1) for i in range(len(df))]


    # Configuration de la palette de couleurs
    palette = sns.color_palette("viridis", len(df['Influenceur']))  # Utilisation d'une palette "viridis"
    color_map = dict(zip(df['Influenceur'], palette))  # Création d'une correspondance entre les influenceurs et les couleurs

    # Affichage des Followers et des Infections
    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 6))

    # Premier graphique: Nombre de followers
    sns.barplot(x='Influenceur', y='followers', hue='Influenceur', data=df, palette=color_map, ax=axs1[0], legend=False)
    axs1[0].set_title('Nombre de Followers par Influenceur')
    axs1[0].set_xticklabels([])

    # Deuxième graphique: Nombre d'infections
    sns.barplot(x='Influenceur', y='infections', hue='Influenceur', data=df, palette=color_map, ax=axs1[1], legend=False)
    axs1[1].set_title('Nombre d\'Infections par Influenceur')
    axs1[1].set_xticklabels([])

    # Ajouter une légende générale pour la figure
    fig1.legend(handles=[plt.Rectangle((0,0),1,1, color=color_map[name]) for name in df['Influenceur']], title='Influenceurs', labels=df['Influenceur'].tolist(), loc='upper right')


    plt.tight_layout()

    # Affichage des Taux de Crédibilité, Activité et Engagement
    fig2, axs2 = plt.subplots(1, 3, figsize=(18, 6))

    # Troisième graphique: Taux d'activité
    scatter = sns.scatterplot(x='Influenceur', y='activity_rate', size='followers', hue='Influenceur', data=df, sizes=(20, 500), legend=False, palette=color_map, ax=axs2[0])
    axs2[0].set_title('Taux d\'Activité par Influenceur')
    axs2[0].set_xticklabels([])

    # Quatrième graphique: Taux de crédibilité
    sns.scatterplot(x='Influenceur', y='credibility_rate', size='followers', hue='Influenceur', data=df, sizes=(20, 500), legend=False, palette=color_map, ax=axs2[1])
    axs2[1].set_title('Taux de Crédibilité par Influenceur')
    axs2[1].set_xticklabels([])

    sns.scatterplot(x='Influenceur', y='engagement_rate',  size='followers', hue='Influenceur', data=df,sizes=(20, 500), legend=False, palette=color_map, ax=axs2[2])
    axs2[2].set_title('Taux d\'Engagement par Influenceur')
    axs2[2].set_xticklabels([])

    # Ajouter une légende générale pour la figure
    fig2.legend(handles=[plt.Rectangle((0,0),1,1, color=color_map[name]) for name in df['Influenceur']], title='Influenceurs', labels=df['Influenceur'].tolist(), loc='upper right')

    plt.tight_layout()

    # Création de la série de temps pour l'évolution des catégories SIR
    ticks = list(range(len(data_sir["S"])))

    # Tracer le graphe de l'évolution des catégories SIR
    plt.figure(figsize=(10, 6))
    plt.plot(ticks, data_sir["S"], label="Susceptibles", color="blue")
    plt.plot(ticks, data_sir["I"], label="Infectés", color="red")
    plt.plot(ticks, data_sir["R"], label="Récupérés", color="green")
    plt.xlabel("Temps")
    plt.ylabel("Nombre d'individus")
    plt.title("Évolution des catégories SIR au cours du temps")
    plt.legend()
    plt.tight_layout()
    plt.show()

def display_results2(data_sir, influencer_data):
    # Conversion de la liste de dictionnaires en DataFrame
    df = pd.DataFrame(influencer_data)


    # Configuration de la palette de couleurs
    palette = sns.color_palette("viridis", len(df['username']))  # Utilisation d'une palette "viridis"
    color_map = dict(zip(df['username'], palette))  # Création d'une correspondance entre les influenceurs et les couleurs

    # Affichage des Followers et des Infections
    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 6))

    # Premier graphique: Nombre de followers
    sns.barplot(x='username', y='followers', hue='username', data=df, palette=color_map, ax=axs1[0], legend=False)
    axs1[0].set_title('Nombre de Followers par Influenceur')
    axs1[0].set_xticklabels([])
    axs1[0].set_xlabel('Influenceurs')

    # Deuxième graphique: Nombre d'infections
    sns.barplot(x='username', y='infections', hue='username', data=df, palette=color_map, ax=axs1[1], legend=False)
    axs1[1].set_title('Nombre d\'Infections par Influenceur')
    axs1[1].set_xticklabels([])
    axs1[1].set_xlabel('Influenceurs')

    # Ajouter une légende générale pour la figure
    fig1.legend(handles=[plt.Rectangle((0,0),1,1, color=color_map[name]) for name in df['username']], title='Influenceurs', labels=df['username'].tolist(), loc='upper right')


    plt.tight_layout()

    # Affichage des Taux de Crédibilité, Activité et Engagement
    fig2, axs2 = plt.subplots(1, 3, figsize=(18, 6))

    # Troisième graphique: Taux d'activité
    scatter = sns.scatterplot(x='username', y='activity_rate', size='followers', hue='username', data=df, sizes=(20, 500), legend=False, palette=color_map, ax=axs2[0])
    axs2[0].set_title('Taux d\'Activité par Influenceur')
    axs2[0].set_xticklabels([])
    axs2[0].set_xlabel('Influenceurs')

    # Quatrième graphique: Taux de crédibilité
    sns.scatterplot(x='username', y='credibility_rate', size='followers', hue='username', data=df, sizes=(20, 500), legend=False, palette=color_map, ax=axs2[1])
    axs2[1].set_title('Taux de Crédibilité par Influenceur')
    axs2[1].set_xticklabels([])
    axs2[1].set_xlabel('Influenceurs')

    sns.scatterplot(x='username', y='engagement_rate',  size='followers', hue='username', data=df,sizes=(20, 500), legend=False, palette=color_map, ax=axs2[2])
    axs2[2].set_title('Taux d\'Engagement par Influenceur')
    axs2[2].set_xticklabels([])
    axs2[2].set_xlabel('Influenceurs')

    # Ajouter une légende générale pour la figure
    fig2.legend(handles=[plt.Rectangle((0,0),1,1, color=color_map[name]) for name in df['username']], title='Influenceurs', labels=df['username'].tolist(), loc='upper right')

    plt.tight_layout()

    # Création de la série de temps pour l'évolution des catégories SIR
    ticks = list(range(len(data_sir["S"])))

    # Tracer le graphe de l'évolution des catégories SIR
    plt.figure(figsize=(10, 6))
    plt.plot(ticks, data_sir["S"], label="Susceptibles", color="blue")
    plt.plot(ticks, data_sir["I"], label="Infectés", color="red")
    plt.plot(ticks, data_sir["R"], label="Récupérés", color="green")
    plt.xlabel("Temps")
    plt.ylabel("Nombre d'individus")
    plt.title("Évolution des catégories SIR au cours du temps")
    plt.legend()
    plt.tight_layout()
    plt.show()


# -------------------------------- Paramètres des scénarios : automate_simulations1 --------------------------------

# paramètres pour tester
params_list = [
    # Scénario 1: Influence de la Haute Crédibilité
    # Influenceurs avec haute crédibilité et taux d'activité moyen, faible engagement
    ([1000, 1000, 1000, 1000, 1000], [0.3, 0.3, 0.4, 0.4, 0.5], [0.95, 0.96, 0.97, 0.98, 0.99], [1.0, 1.5, 2.0, 2.5, 3.0], 5, 1000),
    
    # Scénario 2: Rôle de l'Engagement Elevé
    # Influenceurs avec engagement élevé, crédibilité variée, et taux d'activité varié
    ([500, 400, 300, 200, 100], [0.1, 0.3, 0.5, 0.7, 0.9], [0.65, 0.70, 0.75, 0.80, 0.85], [5.0, 6.0, 7.0, 8.0, 9.0], 5, 5000),
    
    # Scénario 3: Interaction des Influenceurs à Faible Activité
    # Influenceurs avec faible activité, crédibilité modérée, et engagement moyen
    ([250, 250, 250, 250, 250], [0.05, 0.10, 0.15, 0.20, 0.25], [0.55, 0.60, 0.65, 0.70, 0.75], [2.0, 2.5, 3.0, 3.5, 4.0], 5, 2000),
]



# Appeler 'automate_simulations' avec les paramètres de test
#results_df = automate_simulations1(params_list)

# -------------------------------- Paramètres réelles : automate_simulations2 --------------------------------

# Chemin vers le fichier CSV téléchargé
file_path = './metrics.csv'

# Lire le fichier CSV
df = pd.read_csv(file_path)

def automate_simulations2(params_list):
    results_dfs = []  # Liste pour stocker les DataFrame de résultats de chaque scénario
    for i, params in enumerate(params_list):
        # Assurez-vous que 'influencer_usernames' est inclus dans les paramètres si disponible
        data, population, influencer_data = run_simulation(
            followers=params['followers'],
            activity_rates=params['activity_rates'],
            credibility_rates=params['credibility_rates'],
            engagement_rates=params['engagement_rates'],
            num_influencers=params['num_influencers'],
            total_users=params['total_users'],
            influencer_usernames=params.get('influencer_usernames')  # Utilisez .get pour éviter une KeyError si la clé n'existe pas
        )
        
        
        # Préparer les données SIR
        data_sir = prepare_sir_data(data)

        # Créer un DataFrame pour les résultats de ce scénario
        influencer_results_df = pd.DataFrame(influencer_data)

        # Enregistrer le DataFrame dans un fichier CSV
        filename = f"RealData_{i+1}.csv"
        influencer_results_df.to_csv(filename, index=False)
        print(f"Results for scenario of Real Data {i+1} saved to {filename}")

        # Stocker le DataFrame dans la liste
        results_dfs.append(influencer_results_df)

        # Visualiser les résultats pour ce scénario (facultatif si vous ne voulez pas d'affichage graphique ici)
        display_results2(data_sir, influencer_data)

    return results_dfs


def choose_influencers(df, num_influencers=5):
    # Assurer que les colonnes nécessaires sont présentes
    expected_columns = ['username', 'activity_rate_weekly', 'credibility_rate', 'engagement_rate_global','followers_count_normalized_to_1000']
    if not all(column in df.columns for column in expected_columns):
        raise ValueError("Missing one or more required columns in the CSV data.")

    # Choisir aléatoirement cinq influenceurs
    chosen_influencers = df.sample(n=num_influencers)  # Utiliser un seed pour la reproductibilité
    return chosen_influencers

def setup_simulation_parameters(df, num_scenarios=1, total_users=5000):
    scenarios = []
    for _ in range(num_scenarios):
        influencers = choose_influencers(df)
        scenario = {
            'followers': influencers['followers_count_normalized_to_1000'].tolist(),
            'activity_rates': influencers['activity_rate_weekly'].tolist(),
            'credibility_rates': influencers['credibility_rate'].tolist(),
            'engagement_rates': influencers['engagement_rate_global'].tolist(),
            'num_influencers': len(influencers),
            'total_users': total_users,
            'influencer_usernames': influencers['username'].tolist()  # Assurer d'inclure les vrais noms

        }
        scenarios.append(scenario)
    return scenarios

# Préparation des paramètres de simulation basée sur le fichier CSV
params_list = setup_simulation_parameters(df)

# Exécution des simulations et stockage des résultats
results_dfs = automate_simulations2(params_list)

