import networkx
import numpy

def power_law_weighting(alpha, n):
    samples = numpy.random.power(2, n*10)
    samples = sorted(samples)
    total = 0.0
    sums = []
    for i in range(n):
        start = i*len(samples)/n
        stop = (i+1)*len(samples)/n
        sums.append(sum(samples[start:stop]))
        total += sums[-1]

    sums = [float(x/total) for x in sums]

    return sums

def random_pick(choices, p):
    cutoffs = numpy.cumsum(p)
    idx = cutoffs.searchsorted(numpy.random.uniform(0,cutoffs[-1]))
    return choices[idx]

lang_weights = power_law_weighting(2, 6)

languages = ['french','german','russian','chinese','spanish','english']

G = networkx.barabasi_albert_graph(598140,8)

nodes = sorted(G.degree(), key=G.degree().get)

for node in nodes:
    neighbors = G[node].keys()

    msg_weights = power_law_weighting(2, len(neighbors))
    language = random_pick(languages, lang_weights)

    for i in range(len(neighbors)):
        label = 'source_weight'
        if label not in G[node][neighbors[i]]:
            G[node][neighbors[i]][label] = msg_weights[i]
        else:
            G[node][neighbors[i]]['target_weight'] = msg_weights[i]

        label = 'language'
        if label not in G[node][neighbors[i]]:
            G[node][neighbors[i]][label] = language

networkx.write_graphml(G, 'out.graphml')