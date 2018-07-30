from collections import defaultdict

dice = {'ability': '\\AbilityDie',
        'boost' : '\\BoostDie',
        'prof' : '\\ProficiencyDie',
        'setback' : '\\SetbackDie',
        'difficulty' : '\\DifficultyDie',
        'challenge' : '\\ChallengeDie',
        'force' : '\\ForceDie',
        'negset' : '\\NegativeSetbackDie'}

genskills = [('Alchemy', 'Int'),
        ('Athletics', 'Br'),
        ('Cool', 'Pr'),
        ('Coordination', 'Ag'),
        ('Discipline', 'Will'),
        ('Mechanic', 'Int'),
        ('Medicine', 'Int'),
        ('Perception', 'Cun'),
        ('Resilience', 'Br'),
        ('Riding', 'Ag'),
        ('Skulduggery', 'Cun'),
        ('Stealth', 'Ag'),
        ('Streetwise', 'Cun'),
        ('Survival', 'Cun'),
        ('Vigilance', 'Will')]

magicskills = [('Arcane', 'Int'),
               ('Divine', 'Will'),
               ('Primal', 'Cun')]

combatskills = [('Brawl', 'Br'),
                ('Melee--Heavy', 'Br'),
                ('Melee--Light', 'Br'),
                ('Ranged--Light', 'Ag'),
                ('Ranged--Heavy', 'Ag')]

socialskills = [('Charm', 'Pr'),
                ('Coercion', 'Will'),
                ('Deception', 'Cun'),
                ('Leadership', 'Pr'),
                ('Negotiation', 'Pr')]

knowskills = [('Education', 'Int'),
              ('Craft', 'Int'),
              ('Lore', 'Int')]




def render_skill(name, char_name, char_lvl, ranks, career = '', other= [], extras = []):
    #Cool (Pr) & \skilldice{4}{2} \BoostDie & \skill[2]\\
    template = '{0} ({1}){5} & \\skilldice{{{2}}}{{{3}}} {4}  & \\skill[{3}]\\\\'
    # generate the dice names for the extra dice, tack onto general extras
    if career == True:
        career = '*'
    extras = ' '.join([dice[d] for d in other] + extras)
    return template.format(name, char_name, char_lvl,
                        ranks, extras, career)

class GenesysChar(object):
    def __init__(self, name, chars, skill_ranks):
        '''Expect name of character, dict of attributes, default dict of skill ranks'''
        self.name = name
        self.chars = chars
        self.skill_ranks = skill_ranks
    def latex_skills(self):
        '''Return string of latexified skills'''
        table_temp = '''\n\\begin{{GenesysTable}}{{l X[l] X[c]}}
    \\textbf{{{0} Skills}} & Dice Pool & Rank \\\\ \n'''
        s = '''\\begin{multicols}{2}
{\\sffamily'''
        # General
        s += table_temp.format('General')
        g = '\n'.join([render_skill(n, c, self.chars[c], self.skill_ranks[n]) for (n,c) in genskills])
        s += g + '\n\\end{GenesysTable}'
        # Magic
        s += table_temp.format('Magic')
        m = '\n'.join([render_skill(n, c, self.chars[c], self.skill_ranks[n]) for (n,c) in magicskills])
        s += m + '\n\\end{GenesysTable}'
        # New column
        s += '\\vspace*{\\fill}\\columnbreak'
        # Combat
        s += table_temp.format('Combat')
        com = '\n'.join([render_skill(n, c, self.chars[c], self.skill_ranks[n]) for (n,c) in combatskills])
        s += com + '\n\\end{GenesysTable}'
        # Social
        s += table_temp.format('Social')
        soc = '\n'.join([render_skill(n, c, self.chars[c], self.skill_ranks[n]) for (n,c) in socialskills])
        s += soc + '\n\\end{GenesysTable}'
        # Knowledge
        s += table_temp.format('Knowledge')
        soc = '\n'.join([render_skill(n, c, self.chars[c], self.skill_ranks[n]) for (n,c) in knowskills])
        s += soc + '\n\\end{GenesysTable}'
        s += '''}
{\\small{* Indicates a career skill}}
\\end{multicols}'''
        return s



# Testing stuff
debug = True
if debug:
    zeno = GenesysChar('Zeno', {'Br': 3,
                                'Ag': 4,
                                'Pr': 2,
                                'Will':2,
                                'Int':2,
                                'Cun':3},
                defaultdict(int, {'Melee--Light': 2,
                        'Athletics': 2,
                        'Coordination':3,
                        'Discipline':1,
                        'Perception':2,
                        'Skulduggery':3,
                        'Stealth':2,
                        'Streetwise':1,
                        'Survival':2,
                        'Primal':1,
                        'Ranged--Light':3,
                        'Brawl':1,
                        'Coercion':1,
                        'Deception':2,
                        'Lore':1,
                        'Craft':2}))
    #print(zeno.latex_skills())
    with open('zeno.tex','w') as f:
        print(zeno.latex_skills(), file=f)


        
'''
Alchemy (Int) & & \skill\\
Athletics (Br) & & \skill\\
%Cool (Pr) & \faCheck & \skill[1]\\
Cool (Pr) & \skilldice{4}{2} \BoostDie & \skill[2]\\
Coordination (Ag) & \ForceDie & \skill\\
Discipline (Will) & \faCheck & \skill\\
Medicine (Int) & \faCheck & \skill[1]\\
Perception (Cun) & & \skill\\
Resilience (Br) & & \skill\\
Riding (Ag) & & \skill\\
Skulduggery (Cun)* & & \skill\\
Stealth (Ag) & & \skill\\
Streetwise (Cun) & & \skill\\
Survival (Cun) & & \skill[1]\\
Vigilance (Will) & & \skill\\
\end{GenesysTable}

\begin{GenesysTable}{X c X[c]}
\textbf{Magic Skills} & Career? & Rank \\
Divine & \faCheck & \skill[2]\\
\end{GenesysTable}

\vspace*{\fill}

\columnbreak

\begin{GenesysTable}{X c X[c]}
\textbf{Combat Skills} & Career? & Rank \\
Brawl (Br) & & \skill\\
Melee--Heavy (Br) & & \skill\\
Melee--Light (Br) & \faCheck & \skill[1]\\
Ranged (Ag) & & \skill\\

\end{GenesysTable}

\begin{GenesysTable}{X c X[c]}
\textbf{Social Skills} & Career? & Rank \\
Charm (Pr) & \faCheck & \skill[1]\\
Coercion (Will) & \faCheck & \skill\\
Deception (Cun) & & \skill\\
Leadership (Pr) & & \skill\\
Negotiation (Pr) & \faCheck & \skill\\
\end{GenesysTable}

\begin{GenesysTable}{X c X[c]}
\textbf{Knowledge Skills} & Career? & Rank \\
Knowledge (Int) & & \skill\\
\end{GenesysTable}

}
{\small{* Indicates a career skill}}
\end{multicols}
'''

