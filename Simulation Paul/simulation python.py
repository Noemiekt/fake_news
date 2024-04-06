import matplotlib.pyplot as plt
import networkx as nx
import json
import random
import time

with open('fake_news_data.json', 'r') as f:
    data = json.load(f)

G = nx.DiGraph()

for user in data['users']:
    G.add_node(user['user_id'], username=user['username'])

for follow in data['follows']:
    G.add_edge(follow['follower_user_id'], follow['following_user_id'])

def propagation_probability(user_id, post_id):
    post = next(post for post in data['posts'] if post['post_id'] == post_id)
    return 1

def propagate_information(user_id, post_id, is_fake_news, colors, share_count):
    propagated_users = set()
    probability = propagation_probability(user_id, post_id)
    for follow in data['follows']:
        if follow['follower_user_id'] == user_id:
            followed_user_id = follow['following_user_id']
            if followed_user_id != 1 and  followed_user_id != 2 and followed_user_id != 7 and followed_user_id != 10:
                if colors[followed_user_id] is None:
                    if share_count < data['posts'][post_id - 1]['shares']:
                        colors[followed_user_id] = 'red' if is_fake_news else 'blue'
                        propagated_users.add(followed_user_id)
                        share_count += 1
                elif colors[followed_user_id] == 'red' and is_fake_news is False:
                    if share_count < data['posts'][post_id - 1]['shares']:
                        colors[followed_user_id] = 'red' if is_fake_news else 'blue'
                        propagated_users.add(followed_user_id)
                        share_count += 1
                elif colors[followed_user_id] == 'blue' and is_fake_news:
                    if share_count < data['posts'][post_id - 1]['shares']:
                        colors[followed_user_id] = 'red' if is_fake_news else 'blue'
                        propagated_users.add(followed_user_id)
                        share_count += 1
    return propagated_users, share_count

def initialize_colors():
    data_colors = {user['user_id']: None for user in data['users']}
    data_colors[1] = 'purple'
    data_colors[7] = 'purple'
    data_colors[2] = 'yellow'
    data_colors[10] = 'yellow'
    return data_colors

def propagate_post(post, colors):
    user_id = post['user_id']
    post_id = post['post_id']
    is_fake_news = post['is_fake_news']
    share_count = 0
    propagated_users = set([user_id])
    for user_id in propagated_users:
        if colors[user_id] is None:
            colors[user_id] = 'red' if is_fake_news else 'blue'
    node_colors = [colors[node] if colors[node] else 'white' for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, with_labels=False)
    plt.title('Propagation des informations - Poste {}'.format(post_id))
    plt.pause(1)
    while propagated_users:
        new_propagated_users = set()
        for propagated_user in propagated_users:
            new_propagated, share_count = propagate_information(propagated_user, post_id, is_fake_news, colors, share_count)
            new_propagated_users.update(new_propagated)
        propagated_users = new_propagated_users
        for user_id in propagated_users:
            if colors[user_id] is None:
                colors[user_id] = 'red' if is_fake_news else 'blue'
        node_colors = [colors[node] if colors[node] else 'white' for node in G.nodes()]
        nx.draw(G, pos, node_color=node_colors, with_labels=False)
        plt.title('Propagation des informations - Poste {}'.format(post_id))
        plt.pause(1)

plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)

colors = initialize_colors()
for post in data['posts']:
    propagate_post(post, colors)

plt.show()