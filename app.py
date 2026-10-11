#!/usr/bin/env python3
"""
Political Science Learning App — Interactive Political Ideologies Explorer
Built with PySide6
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QStackedWidget, QScrollArea,
    QComboBox, QButtonGroup, QProgressBar, QDialog, QFrame,
    QSizePolicy, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QPalette, QPolygonF
)

# ============================================================================
# DATA
# ============================================================================

IDEOLOGIES = [
    {
        "name": "Liberalism",
        "color": "#4A90D9",
        "econ": 2, "social": -5,
        "summary": "Emphasizes individual liberty, equality, and democratic governance with a regulated market economy.",
        "description": (
            "Liberalism is a political and moral philosophy based on liberty, consent of the governed, "
            "and equality before the law. Liberals advocate for civil rights, democracy, secularism, "
            "and political freedom. They generally support a mixed economy with government intervention "
            "to correct market failures and provide social safety nets, while maintaining free enterprise."
        ),
        "principles": [
            "Individual liberty and freedom",
            "Equality of opportunity",
            "Rule of law and constitutional government",
            "Free markets with sensible regulation",
            "Protection of civil and human rights",
            "Democratic governance and pluralism"
        ],
        "thinkers": ["John Locke", "John Stuart Mill", "Immanuel Kant", "John Rawls", "Adam Smith"],
        "origin": "17th century Enlightenment"
    },
    {
        "name": "Conservatism",
        "color": "#8B6914",
        "econ": 5, "social": 4,
        "summary": "Values tradition, social stability, and gradual change over radical reform.",
        "description": (
            "Conservatism is a political and social philosophy that promotes retaining traditional social "
            "institutions and values. Conservatives seek to preserve a range of institutions such as religion, "
            "the family, and traditional morality. They tend to favor free markets, limited government "
            "intervention in the economy, and strong national defense."
        ),
        "principles": [
            "Preservation of tradition and customs",
            "Social stability and order",
            "Limited but effective government",
            "Free enterprise and fiscal responsibility",
            "Strong national defense",
            "Skepticism of rapid social change"
        ],
        "thinkers": ["Edmund Burke", "Russell Kirk", "Michael Oakeshott", "Thomas Aquinas", "Barry Goldwater"],
        "origin": "18th century (reaction to French Revolution)"
    },
    {
        "name": "Socialism",
        "color": "#DC143C",
        "econ": -7, "social": 2,
        "summary": "Advocates social ownership and democratic control of the means of production.",
        "description": (
            "Socialism is a range of economic and social systems characterized by social ownership of the "
            "means of production and workers' self-management. Socialists argue that capitalism creates "
            "inequality and exploitation, and that resources should be allocated based on need rather than "
            "profit. Democratic socialism seeks to achieve these goals through democratic means."
        ),
        "principles": [
            "Social ownership of production",
            "Economic equality and redistribution",
            "Workers' rights and self-management",
            "Opposition to capitalist exploitation",
            "Universal social services",
            "Democratic planning of the economy"
        ],
        "thinkers": ["Karl Marx", "Friedrich Engels", "Rosa Luxemburg", "Eduard Bernstein", "Antonio Gramsci"],
        "origin": "19th century Industrial Revolution"
    },
    {
        "name": "Communism",
        "color": "#8B0000",
        "econ": -9, "social": 7,
        "summary": "Envisions a classless, stateless society with common ownership of all property.",
        "description": (
            "Communism is a philosophical, social, political, and economic ideology whose ultimate goal "
            "is the establishment of a communist society — a classless, stateless society where the means "
            "of production are commonly owned. Marxist-Leninist interpretations advocate for a vanguard "
            "party leading a revolution to overthrow capitalism and establish a transitional socialist state."
        ),
        "principles": [
            "Abolition of private property",
            "Classless society as ultimate goal",
            "Central planning of economy",
            "Dictatorship of the proletariat (transitional)",
            "From each according to ability, to each according to need",
            "Revolutionary transformation of society"
        ],
        "thinkers": ["Karl Marx", "Friedrich Engels", "Vladimir Lenin", "Leon Trotsky", "Mao Zedong"],
        "origin": "1848 (The Communist Manifesto)"
    },
    {
        "name": "Libertarianism",
        "color": "#FFD700",
        "econ": 8, "social": -8,
        "summary": "Maximizes individual freedom and minimizes state power in all areas of life.",
        "description": (
            "Libertarianism is a political philosophy that upholds liberty as a core principle. Libertarians "
            "seek to maximize political freedom and autonomy, emphasizing freedom of choice, voluntary "
            "association, and individual judgment. They advocate for minimal government intervention in both "
            "economic and personal affairs, supporting free markets and civil liberties."
        ),
        "principles": [
            "Maximum individual liberty",
            "Minimal government intervention",
            "Free markets without regulation",
            "Self-ownership and property rights",
            "Non-aggression principle",
            "Voluntary association in all spheres"
        ],
        "thinkers": ["Murray Rothbard", "Ayn Rand", "Robert Nozick", "Friedrich Hayek", "Ludwig von Mises"],
        "origin": "Mid-20th century"
    },
    {
        "name": "Fascism",
        "color": "#555555",
        "econ": 3, "social": 9,
        "summary": "An authoritarian ultranationalist ideology emphasizing dictatorial power and suppression of opposition.",
        "description": (
            "Fascism is a far-right, authoritarian, ultranationalist political ideology characterized by "
            "dictatorial power, forcible suppression of opposition, and strong regimentation of society "
            "and the economy. Fascism rose to prominence in early 20th-century Europe, emphasizing militarism, "
            "national rebirth, and the superiority of the nation or race."
        ),
        "principles": [
            "Ultra-nationalism and national rebirth",
            "Authoritarian leadership (dictatorship)",
            "Suppression of political opposition",
            "Militarism and imperial expansion",
            "State control of economy (corporatism)",
            "Cult of tradition and cultural purity"
        ],
        "thinkers": ["Benito Mussolini", "Adolf Hitler", "Giovanni Gentile", "Corneliu Codreanu"],
        "origin": "Early 20th century Italy"
    },
    {
        "name": "Anarchism",
        "color": "#333333",
        "econ": -6, "social": -9,
        "summary": "Opposes all involuntary, coercive forms of hierarchy and authority.",
        "description": (
            "Anarchism is a political philosophy that advocates self-governed societies based on voluntary "
            "institutions. Anarchists oppose all forms of involuntary and coercive hierarchy, including "
            "the state, capitalism, and organized religion. They propose various forms of self-organization "
            "including communes, syndicates, and mutual aid networks."
        ),
        "principles": [
            "Abolition of the state and government",
            "Voluntary cooperation and mutual aid",
            "Anti-authoritarianism in all forms",
            "Direct democracy and consensus",
            "Worker self-management",
            "Opposition to all forms of oppression"
        ],
        "thinkers": ["Mikhail Bakunin", "Peter Kropotkin", "Emma Goldman", "Pierre-Joseph Proudhon", "Noam Chomsky"],
        "origin": "19th century"
    },
    {
        "name": "Social Democracy",
        "color": "#E8742A",
        "econ": -4, "social": -2,
        "summary": "Supports a mixed economy with strong social welfare programs within a democratic framework.",
        "description": (
            "Social democracy is a political, social, and economic philosophy that supports economic and "
            "social interventions to promote social justice within the framework of a liberal democratic "
            "polity and a capitalist-oriented mixed economy. Social democrats advocate for a balance between "
            "market efficiency and social equity through regulation, welfare programs, and collective bargaining."
        ),
        "principles": [
            "Mixed economy with regulation",
            "Comprehensive welfare state",
            "Progressive taxation",
            "Strong labor rights and unions",
            "Social justice and equality of opportunity",
            "Reformist rather than revolutionary change"
        ],
        "thinkers": ["Eduard Bernstein", "Karl Kautsky", "Clement Attlee", "Olof Palme", "Gösta Esping-Andersen"],
        "origin": "Late 19th / Early 20th century"
    },
    {
        "name": "Neoliberalism",
        "color": "#20B2AA",
        "econ": 7, "social": -1,
        "summary": "Emphasizes free-market capitalism, deregulation, privatization, and reduced government spending.",
        "description": (
            "Neoliberalism is a political and economic ideology that advocates for free-market capitalism, "
            "deregulation, privatization, and reduction in government spending. Neoliberals believe that "
            "market forces are the most efficient way to allocate resources and that government intervention "
            "typically creates more problems than it solves. It became dominant in the late 20th century."
        ),
        "principles": [
            "Free market capitalism",
            "Deregulation and privatization",
            "Free trade and globalization",
            "Fiscal austerity and small government",
            "Individual responsibility",
            "Market-based solutions to social problems"
        ],
        "thinkers": ["Milton Friedman", "Friedrich Hayek", "Ronald Reagan", "Margaret Thatcher", "Alan Greenspan"],
        "origin": "1930s (revived in 1970s–80s)"
    },
    {
        "name": "Progressivism",
        "color": "#9B59B6",
        "econ": -3, "social": -6,
        "summary": "Seeks social progress through political reform, equality, and evidence-based policy.",
        "description": (
            "Progressivism is a political philosophy that emphasizes social reform, equality, and the use "
            "of government to address social problems. Progressives advocate for civil rights, environmental "
            "protection, economic fairness, and social justice. They believe society can and should improve "
            "through conscious reform efforts and evidence-based policy."
        ),
        "principles": [
            "Social and political reform",
            "Civil rights and social justice",
            "Environmental protection",
            "Economic fairness and regulation",
            "Government as a force for good",
            "Evidence-based policy making"
        ],
        "thinkers": ["John Dewey", "Theodore Roosevelt", "Woodrow Wilson", "Jane Addams", "Bernie Sanders"],
        "origin": "Late 19th century"
    },
    {
        "name": "Nationalism",
        "color": "#4169E1",
        "econ": 1, "social": 6,
        "summary": "Prioritizes national identity, sovereignty, and interests above international cooperation.",
        "description": (
            "Nationalism is an ideology that emphasizes loyalty, devotion, or allegiance to a nation or "
            "nation-state, asserting that the nation should be congruent with the state. Nationalists "
            "prioritize national interests, culture, and sovereignty, often advocating for protectionist "
            "economic policies and strong borders."
        ),
        "principles": [
            "National sovereignty and independence",
            "Cultural preservation and national pride",
            "Protectionist economic policies",
            "Strong borders and controlled immigration",
            "National self-determination",
            "Prioritizing national interests globally"
        ],
        "thinkers": ["Johann Gottfried Herder", "Giuseppe Mazzini", "Charles Maurras", "Ernest Renan"],
        "origin": "18th–19th century"
    },
    {
        "name": "Environmentalism",
        "color": "#2ECC71",
        "econ": -4, "social": -4,
        "summary": "Focused on protecting the natural environment through political action and systemic change.",
        "description": (
            "Environmentalism is a broad philosophy and social movement regarding concerns for environmental "
            "protection and improvement. Green politics advocates for sustainability, ecological wisdom, "
            "social justice, and grassroots democracy. Environmentalists often support regulation of "
            "polluting industries, transition to renewable energy, and rethinking economic growth."
        ),
        "principles": [
            "Ecological sustainability",
            "Climate action and renewable energy",
            "Conservation of natural resources",
            "Social justice and equity",
            "Grassroots democracy",
            "Intergenerational responsibility"
        ],
        "thinkers": ["Rachel Carson", "Aldo Leopold", "Arne Næss", "Murray Bookchin", "Petra Kelly"],
        "origin": "1960s–70s environmental movement"
    },
]

QUIZ_QUESTIONS = [
    {"text": "The government should provide universal healthcare funded by taxpayers.", "econ": -1.0, "social": 0.3},
    {"text": "Free markets are the most efficient way to allocate resources in society.", "econ": 1.0, "social": -0.2},
    {"text": "Strong law and order policies are essential for a stable society.", "econ": 0.2, "social": 1.0},
    {"text": "People should have the freedom to make their own lifestyle choices without government interference.", "econ": -0.2, "social": -1.0},
    {"text": "Wealth should be redistributed from the rich to reduce economic inequality.", "econ": -1.0, "social": 0.2},
    {"text": "National security concerns can justify increased surveillance of citizens.", "econ": 0.2, "social": 1.0},
    {"text": "Private property rights are fundamental and should be strongly protected by law.", "econ": 1.0, "social": -0.3},
    {"text": "The state should regulate businesses to protect workers and consumers.", "econ": -0.8, "social": 0.5},
    {"text": "Military intervention is sometimes necessary to maintain international order.", "econ": 0.1, "social": 0.8},
    {"text": "Education at all levels should be free and publicly funded.", "econ": -0.9, "social": 0.2},
    {"text": "Traditional values and customs should be preserved in society.", "econ": 0.1, "social": 0.9},
    {"text": "Workers should have a democratic say in how their companies are run.", "econ": -0.7, "social": -0.3},
    {"text": "Lower taxes stimulate economic growth and ultimately benefit everyone.", "econ": 0.9, "social": -0.1},
    {"text": "Censorship is sometimes necessary to protect society from harmful ideas.", "econ": -0.1, "social": 1.0},
    {"text": "Immigration should be strictly controlled to protect national identity and security.", "econ": 0.3, "social": 0.8},
    {"text": "Government should play a minimal role in the economy and let markets self-regulate.", "econ": 1.0, "social": -0.5},
    {"text": "All people should have equal rights regardless of their background or identity.", "econ": -0.3, "social": -0.9},
    {"text": "Corporations have too much influence over government policy and must be restrained.", "econ": -0.6, "social": -0.2},
    {"text": "Civil liberties should never be restricted, even during national emergencies.", "econ": 0.0, "social": -1.0},
    {"text": "Essential services like water, electricity, and transportation should be publicly owned.", "econ": -0.9, "social": 0.3},
    {"text": "International organizations threaten national sovereignty and should have less power.", "econ": 0.3, "social": 0.7},
    {"text": "People should be free to express any opinion, even if others find it offensive.", "econ": 0.1, "social": -0.9},
    {"text": "A progressive tax system with higher rates for higher incomes is fair and necessary.", "econ": -0.8, "social": 0.1},
    {"text": "The government should guarantee a minimum standard of living for all citizens.", "econ": -0.8, "social": 0.4},
    {"text": "Competition and the profit motive are the primary drivers of innovation and prosperity.", "econ": 0.9, "social": -0.2},
]

GLOSSARY = {
    "Capitalism": "An economic system based on private ownership of the means of production and their operation for profit, characterized by voluntary exchange, competitive markets, and wage labor.",
    "Socialism": "An economic and political system where the means of production are socially owned, aiming to reduce inequality and prioritize need over profit.",
    "Democracy": "A system of government by the whole population, typically through elected representatives, with majority rule and protection of minority rights.",
    "Authoritarianism": "A form of government characterized by strong central power, limited political pluralism, and restricted civil liberties.",
    "Libertarianism": "A political philosophy that emphasizes individual liberty as the primary political value and advocates minimal state intervention.",
    "Collectivism": "The principle of prioritizing the group over the individual, often associated with communal ownership and cooperative social organization.",
    "Individualism": "The moral stance and philosophy that emphasizes the moral worth and rights of the individual over collective or state interests.",
    "Populism": "A political approach that claims to represent the common people against corrupt or self-serving elites, often using emotionally charged rhetoric.",
    "Secularism": "The principle of separating government institutions and policies from religious institutions and beliefs.",
    "Federalism": "A system of government in which sovereignty is divided between a central authority and constituent political units (states, provinces).",
    "Globalism": "The policy or advocacy of planning economic and foreign policy on a global basis, supporting international cooperation and integration.",
    "Welfare State": "A system in which the government undertakes responsibility for the social and economic well-being of its citizens through social safety nets.",
    "Laissez-faire": "An economic philosophy of free-market capitalism that opposes government intervention in business affairs and commercial regulation.",
    "Totalitarianism": "A system of government that is centralized and dictatorial, requiring complete subservience to the state in all aspects of life.",
    "Pluralism": "A political system in which multiple groups, interests, and viewpoints coexist and compete within a democratic framework.",
    "Meritocracy": "A system in which advancement is based on individual ability, effort, and achievement rather than birthright or wealth.",
    "Proletariat": "In Marxist theory, the class of wage earners who do not own the means of production and must sell their labor to survive.",
    "Bourgeoisie": "In Marxist theory, the capitalist class who own the means of production and derive profit from the labor of the proletariat.",
    "Class Struggle": "The political and economic conflict between the working class and the owning class, central to Marxist theory of historical development.",
    "Means of Production": "The facilities, resources, and infrastructure used to produce goods and services in a society.",
    "Hegemony": "Political, cultural, or ideological dominance of one group over others, often maintained through consent rather than force.",
    "Social Contract": "An implicit agreement among individuals to form a society and government, surrendering some freedoms for protection and order.",
    "Separation of Powers": "The division of government responsibilities into distinct branches to prevent the concentration of power.",
    "Rule of Law": "The principle that all individuals and institutions are subject to and accountable to law that is fairly applied and enforced.",
    "Civil Liberties": "Fundamental individual rights and freedoms protected from government infringement, such as freedom of speech and religion.",
}

TIMELINE_EVENTS = [
    {"year": 1215, "title": "Magna Carta", "desc": "Limited monarchic power, foundation for rule of law and constitutionalism.", "color": "#4A90D9"},
    {"year": 1513, "title": "The Prince (Machiavelli)", "desc": "Foundational text on political realism and power dynamics.", "color": "#555555"},
    {"year": 1651, "title": "Leviathan (Hobbes)", "desc": "Social contract theory arguing for strong sovereign authority.", "color": "#8B6914"},
    {"year": 1689, "title": "Two Treatises (Locke)", "desc": "Foundation of liberalism: natural rights, consent of the governed.", "color": "#4A90D9"},
    {"year": 1776, "title": "American Revolution", "desc": "Liberal democratic principles put into practice.", "color": "#4A90D9"},
    {"year": 1789, "title": "French Revolution", "desc": "Radical rethinking of political order; birth of left-right spectrum.", "color": "#DC143C"},
    {"year": 1790, "title": "Reflections on the Revolution (Burke)", "desc": "Founding text of modern conservatism.", "color": "#8B6914"},
    {"year": 1848, "title": "Communist Manifesto", "desc": "Marx and Engels lay out communist theory and class struggle.", "color": "#8B0000"},
    {"year": 1867, "title": "Das Kapital (Marx)", "desc": "Comprehensive critique of political economy and capitalism.", "color": "#8B0000"},
    {"year": 1869, "title": "On Liberty (Mill)", "desc": "Classic defense of individual freedom and liberal principles.", "color": "#4A90D9"},
    {"year": 1922, "title": "March on Rome", "desc": "Mussolini's fascists take power in Italy.", "color": "#555555"},
    {"year": 1933, "title": "Rise of Nazism", "desc": "Hitler appointed Chancellor; totalitarian state established in Germany.", "color": "#555555"},
    {"year": 1944, "title": "The Road to Serfdom (Hayek)", "desc": "Foundational neoliberal text warning against central planning.", "color": "#20B2AA"},
    {"year": 1945, "title": "Post-War Social Democracy", "desc": "Welfare states established across Western Europe.", "color": "#E8742A"},
    {"year": 1949, "title": "Chinese Communist Revolution", "desc": "Mao establishes the People's Republic of China.", "color": "#8B0000"},
    {"year": 1962, "title": "Silent Spring (Carson)", "desc": "Catalyst for the modern environmental movement.", "color": "#2ECC71"},
    {"year": 1968, "title": "Global Protests", "desc": "Anti-war, civil rights, and counterculture movements reshape politics.", "color": "#9B59B6"},
    {"year": 1971, "title": "Anarchy, State, and Utopia (Nozick)", "desc": "Libertarian response to redistributive justice theories.", "color": "#FFD700"},
    {"year": 1979, "title": "Thatcher / Reagan Era", "desc": "Neoliberal policies dominate: deregulation, privatization, free markets.", "color": "#20B2AA"},
    {"year": 1989, "title": "Fall of the Berlin Wall", "desc": "Collapse of Soviet-style communism across Eastern Europe.", "color": "#DC143C"},
    {"year": 1999, "title": "Seattle WTO Protests", "desc": "Anti-globalization movement gains visibility.", "color": "#2ECC71"},
    {"year": 2011, "title": "Occupy Wall Street", "desc": "Protest against economic inequality; 'We are the 99%'.", "color": "#DC143C"},
    {"year": 2016, "title": "Populist Surges", "desc": "Brexit and Trump's election mark a nationalist-populist wave.", "color": "#4169E1"},
    {"year": 2019, "title": "Climate Activism", "desc": "Global climate strikes push environmentalism into mainstream politics.", "color": "#2ECC71"},
]


# ============================================================================
# CUSTOM WIDGETS
# ============================================================================

class CompassWidget(QWidget):
    """Custom-painted political compass chart."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_econ = None
        self.user_social = None
        self.hovered_ideology = None
        self.setMinimumSize(380, 380)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

    def set_user_position(self, econ, social):
        self.user_econ = econ
        self.user_social = social
        self.update()

    def _map(self, econ, social, rect):
        x = rect.x() + (econ + 10) / 20.0 * rect.width()
        y = rect.y() + (10 - social) / 20.0 * rect.height()
        return x, y

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        size = min(w, h) - 70
        if size < 100:
            p.end()
            return
        ox = (w - size) / 2
        oy = (h - size) / 2
        rect = QRectF(ox, oy, size, size)
        half = size / 2

        # Quadrant backgrounds
        p.fillRect(QRectF(ox, oy, half, half), QColor(200, 80, 80, 30))
        p.fillRect(QRectF(ox + half, oy, half, half), QColor(80, 80, 200, 30))
        p.fillRect(QRectF(ox, oy + half, half, half), QColor(80, 180, 80, 30))
        p.fillRect(QRectF(ox + half, oy + half, half, half), QColor(200, 200, 60, 30))

        # Grid
        p.setPen(QPen(QColor(255, 255, 255, 20), 1, Qt.DotLine))
        for i in range(1, 20):
            x = ox + i * size / 20
            p.drawLine(QPointF(x, oy), QPointF(x, oy + size))
            y = oy + i * size / 20
            p.drawLine(QPointF(ox, y), QPointF(ox + size, y))

        # Main axes
        p.setPen(QPen(QColor(255, 255, 255, 80), 2))
        p.drawLine(QPointF(ox, oy + half), QPointF(ox + size, oy + half))
        p.drawLine(QPointF(ox + half, oy), QPointF(ox + half, oy + size))

        # Arrows
        p.drawLine(QPointF(ox + size, oy + half), QPointF(ox + size - 8, oy + half - 4))
        p.drawLine(QPointF(ox + size, oy + half), QPointF(ox + size - 8, oy + half + 4))
        p.drawLine(QPointF(ox + half, oy), QPointF(ox + half - 4, oy + 8))
        p.drawLine(QPointF(ox + half, oy), QPointF(ox + half + 4, oy + 8))

        # Quadrant labels
        p.setPen(QColor(200, 200, 200, 80))
        f = QFont("Segoe UI", 8)
        f.setItalic(True)
        p.setFont(f)
        p.drawText(QRectF(ox + 4, oy + 4, half - 8, 18), Qt.AlignLeft | Qt.AlignTop, "Auth-Left")
        p.drawText(QRectF(ox + half + 4, oy + 4, half - 8, 18), Qt.AlignRight | Qt.AlignTop, "Auth-Right")
        p.drawText(QRectF(ox + 4, oy + size - 22, half - 8, 18), Qt.AlignLeft | Qt.AlignBottom, "Lib-Left")
        p.drawText(QRectF(ox + half + 4, oy + size - 22, half - 8, 18), Qt.AlignRight | Qt.AlignBottom, "Lib-Right")

        # Axis labels
        p.setPen(QColor(220, 220, 220))
        f = QFont("Segoe UI", 10, QFont.Bold)
        p.setFont(f)
        p.drawText(QRectF(ox - 5, oy + half - 12, 40, 24), Qt.AlignRight | Qt.AlignVCenter, "LEFT")
        p.drawText(QRectF(ox + size - 35, oy + half - 12, 45, 24), Qt.AlignLeft | Qt.AlignVCenter, "RIGHT")
        p.drawText(QRectF(ox + half - 50, oy - 20, 100, 18), Qt.AlignCenter, "AUTHORITARIAN")
        p.drawText(QRectF(ox + half - 50, oy + size + 4, 100, 18), Qt.AlignCenter, "LIBERTARIAN")

        # Ideology dots
        f = QFont("Segoe UI", 7)
        p.setFont(f)
        for ideo in IDEOLOGIES:
            sx, sy = self._map(ideo["econ"], ideo["social"], rect)
            color = QColor(ideo["color"])
            is_hovered = (self.hovered_ideology == ideo["name"])
            r = 7 if is_hovered else 5
            if is_hovered:
                p.setBrush(QBrush(color.lighter(130)))
                p.setPen(QPen(QColor(255, 255, 255, 180), 2))
            else:
                p.setBrush(QBrush(color))
                p.setPen(QPen(color.darker(150), 1))
            p.drawEllipse(QPointF(sx, sy), r, r)
            p.setPen(QColor(220, 220, 220, 200 if is_hovered else 160))
            if is_hovered:
                bold_f = QFont("Segoe UI", 8, QFont.Bold)
                p.setFont(bold_f)
            p.drawText(QPointF(sx + 10, sy + 4), ideo["name"])
            if is_hovered:
                p.setFont(f)

        # User marker
        if self.user_econ is not None:
            ux, uy = self._map(self.user_econ, self.user_social, rect)
            for r in range(18, 6, -2):
                alpha = int(50 * (18 - r) / 12)
                p.setBrush(QBrush(QColor(255, 80, 80, alpha)))
                p.setPen(Qt.NoPen)
                p.drawEllipse(QPointF(ux, uy), r, r)
            p.setBrush(QBrush(QColor(255, 60, 60)))
            p.setPen(QPen(QColor(255, 255, 255), 2.5))
            p.drawEllipse(QPointF(ux, uy), 9, 9)
            p.setPen(QColor(255, 255, 255))
            f2 = QFont("Segoe UI", 9, QFont.Bold)
            p.setFont(f2)
            p.drawText(QPointF(ux + 14, uy + 5), "YOU")

        # Border
        p.setPen(QPen(QColor(255, 255, 255, 30), 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(rect)
        p.end()

    def mouseMoveEvent(self, event):
        w, h = self.width(), self.height()
        size = min(w, h) - 70
        if size < 100:
            return
        ox = (w - size) / 2
        oy = (h - size) / 2
        rect = QRectF(ox, oy, size, size)

        mx, my = event.position().x(), event.position().y()
        closest = None
        closest_dist = 20
        for ideo in IDEOLOGIES:
            sx, sy = self._map(ideo["econ"], ideo["social"], rect)
            dist = math.hypot(mx - sx, my - sy)
            if dist < closest_dist:
                closest = ideo["name"]
                closest_dist = dist

        if closest != self.hovered_ideology:
            self.hovered_ideology = closest
            self.update()


class RadarChartWidget(QWidget):
    """Radar/spider chart showing distance to all ideologies."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.distances = {}
        self.user_econ = 0
        self.user_social = 0
        self.hovered = None
        self.setMinimumSize(350, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

    def set_data(self, user_econ, user_social):
        self.user_econ = user_econ
        self.user_social = user_social
        self.distances = {}
        for ideo in IDEOLOGIES:
            d = math.hypot(ideo["econ"] - user_econ, ideo["social"] - user_social)
            self.distances[ideo["name"]] = {
                "distance": d,
                "color": ideo["color"],
                "econ": ideo["econ"],
                "social": ideo["social"],
            }
        self.update()

    def paintEvent(self, event):
        if not self.distances:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        size = min(w, h) - 80
        if size < 100:
            p.end()
            return

        cx = w / 2
        cy = h / 2
        radius = size / 2

        n = len(self.distances)
        angle_step = 2 * math.pi / n
        max_dist = 20 * math.sqrt(2)

        # Concentric rings
        for ring in range(1, 5):
            r = radius * ring / 4
            p.setPen(QPen(QColor(255, 255, 255, 25), 1))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(QPointF(cx, cy), r, r)

        sorted_items = sorted(self.distances.items(), key=lambda x: x[1]["distance"])

        p.setPen(QPen(QColor(255, 255, 255, 30), 1))
        label_font = QFont("Segoe UI", 7)
        p.setFont(label_font)

        angles = {}
        for i, (name, data) in enumerate(sorted_items):
            angle = -math.pi / 2 + i * angle_step
            angles[name] = angle

            ex = cx + radius * math.cos(angle)
            ey = cy + radius * math.sin(angle)
            p.drawLine(QPointF(cx, cy), QPointF(ex, ey))

            lx = cx + (radius + 16) * math.cos(angle)
            ly = cy + (radius + 16) * math.sin(angle)

            is_hovered = (self.hovered == name)
            color = QColor(data["color"]) if is_hovered else QColor(180, 180, 180)
            if is_hovered:
                bold_f = QFont("Segoe UI", 8, QFont.Bold)
                p.setFont(bold_f)
            else:
                p.setFont(label_font)
            p.setPen(color)

            rect = QRectF(lx - 50, ly - 8, 100, 16)
            p.drawText(rect, Qt.AlignCenter, name)

        # Polygon
        points = []
        for name, data in sorted_items:
            angle = angles[name]
            normalized = 1.0 - (data["distance"] / max_dist)
            normalized = max(0.05, min(1.0, normalized))
            r = radius * normalized
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append(QPointF(px, py))

        polygon = QPolygonF(points)
        p.setBrush(QBrush(QColor(233, 69, 96, 40)))
        p.setPen(QPen(QColor(233, 69, 96, 160), 2))
        p.drawPolygon(polygon)

        # Vertex dots
        for i, (name, data) in enumerate(sorted_items):
            is_hovered = (self.hovered == name)
            r = 5 if is_hovered else 3
            color = QColor(data["color"])
            p.setBrush(QBrush(color.lighter(130) if is_hovered else color))
            p.setPen(QPen(QColor(255, 255, 255, 180 if is_hovered else 100), 1.5))
            p.drawEllipse(points[i], r, r)

        # Center dot
        p.setBrush(QBrush(QColor(233, 69, 96)))
        p.setPen(QPen(QColor(255, 255, 255), 2))
        p.drawEllipse(QPointF(cx, cy), 4, 4)

        # Title
        p.setPen(QColor(200, 200, 200))
        title_font = QFont("Segoe UI", 10, QFont.Bold)
        p.setFont(title_font)
        p.drawText(QRectF(0, 4, w, 20), Qt.AlignCenter, "Ideology Affinity Radar")

        # Hover tooltip
        if self.hovered and self.hovered in self.distances:
            d = self.distances[self.hovered]["distance"]
            pct = max(0, (1.0 - d / max_dist) * 100)
            tip_font = QFont("Segoe UI", 9)
            p.setFont(tip_font)
            p.setPen(QColor(255, 255, 255))
            tip_text = f"{self.hovered}: {pct:.0f}% match"
            p.drawText(QRectF(cx - 80, cy + 12, 160, 18), Qt.AlignCenter, tip_text)

        p.end()

    def mouseMoveEvent(self, event):
        if not self.distances:
            return

        w, h = self.width(), self.height()
        size = min(w, h) - 80
        if size < 100:
            return
        cx = w / 2
        cy = h / 2
        radius = size / 2

        n = len(self.distances)
        angle_step = 2 * math.pi / n
        max_dist = 20 * math.sqrt(2)
        sorted_items = sorted(self.distances.items(), key=lambda x: x[1]["distance"])

        mx, my = event.position().x(), event.position().y()
        closest = None
        closest_dist = 25

        for i, (name, data) in enumerate(sorted_items):
            angle = -math.pi / 2 + i * angle_step
            normalized = 1.0 - (data["distance"] / max_dist)
            normalized = max(0.05, min(1.0, normalized))
            r = radius * normalized
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            dist = math.hypot(mx - px, my - py)
            if dist < closest_dist:
                closest = name
                closest_dist = dist

        if closest != self.hovered:
            self.hovered = closest
            self.update()


class ClickableCard(QFrame):
    clicked = Signal(dict)

    def __init__(self, ideology, parent=None):
        super().__init__(parent)
        self.ideology = ideology
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            ClickableCard {{
                background-color: #1e2a3a;
                border: 2px solid {ideology['color']}33;
                border-radius: 12px;
                padding: 10px;
            }}
            ClickableCard:hover {{
                background-color: #243447;
                border-color: {ideology['color']}99;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        header = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {ideology['color']}; font-size: 18px;")
        name = QLabel(ideology["name"])
        name.setStyleSheet("font-size: 15px; font-weight: bold; color: #eee;")
        header.addWidget(dot)
        header.addWidget(name)
        header.addStretch()
        layout.addLayout(header)

        summary = QLabel(ideology["summary"])
        summary.setWordWrap(True)
        summary.setStyleSheet("color: #bbb; font-size: 11px; line-height: 1.4;")
        layout.addWidget(summary)

        pos = QHBoxLayout()
        econ_lbl = QLabel(f"Econ: {ideology['econ']:+d}")
        soc_lbl = QLabel(f"Social: {ideology['social']:+d}")
        econ_lbl.setStyleSheet("color: #888; font-size: 10px;")
        soc_lbl.setStyleSheet("color: #888; font-size: 10px;")
        pos.addWidget(econ_lbl)
        pos.addStretch()
        pos.addWidget(soc_lbl)
        layout.addLayout(pos)
        self.setFixedHeight(135)

    def mousePressEvent(self, event):
        self.clicked.emit(self.ideology)
        super().mousePressEvent(event)


class IdeologyDetailDialog(QDialog):
    def __init__(self, ideology, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{ideology['name']} — Details")
        self.setMinimumSize(560, 700)
        self.setStyleSheet("QDialog { background-color: #1a1a2e; } QLabel { color: #ddd; }")

        outer = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #1a1a2e; }")

        content = QWidget()
        content.setStyleSheet("background-color: #1a1a2e;")
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        # Header banner
        banner = QFrame()
        banner.setStyleSheet(f"""
            QFrame {{ background-color: {ideology['color']}22; 
                      border-left: 4px solid {ideology['color']};
                      border-radius: 0 8px 8px 0; padding: 12px; }}
        """)
        banner_layout = QVBoxLayout(banner)
        
        title = QLabel(ideology["name"])
        title.setStyleSheet(f"font-size: 26px; font-weight: bold; color: {ideology['color']};")
        banner_layout.addWidget(title)
        
        origin = QLabel(f"📍 Origin: {ideology['origin']}")
        origin.setStyleSheet("color: #999; font-size: 12px;")
        banner_layout.addWidget(origin)
        
        pos_text = QLabel(f"📐 Economic: {ideology['econ']:+d}  |  Social: {ideology['social']:+d}")
        pos_text.setStyleSheet("color: #bbb; font-size: 12px;")
        banner_layout.addWidget(pos_text)
        
        layout.addWidget(banner)

        # Mini compass
        mini_compass = CompassWidget()
        mini_compass.set_user_position(ideology["econ"], ideology["social"])
        mini_compass.setFixedHeight(260)
        layout.addWidget(mini_compass)

        desc = QLabel(ideology["description"])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #ccc; font-size: 13px; line-height: 1.6;")
        layout.addWidget(desc)

        layout.addWidget(self._section("🔑 Key Principles"))
        for pr in ideology["principles"]:
            lbl = QLabel(f"  •  {pr}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #bbb; font-size: 12px;")
            layout.addWidget(lbl)

        layout.addWidget(self._section("👤 Notable Thinkers"))
        for th in ideology["thinkers"]:
            lbl = QLabel(f"  •  {th}")
            lbl.setStyleSheet("color: #bbb; font-size: 12px;")
            layout.addWidget(lbl)

        # Nearby ideologies
        layout.addWidget(self._section("📍 Nearby Ideologies on Compass"))
        nearby = []
        for other in IDEOLOGIES:
            if other["name"] != ideology["name"]:
                d = math.hypot(other["econ"] - ideology["econ"], other["social"] - ideology["social"])
                nearby.append((other, d))
        nearby.sort(key=lambda x: x[1])
        for other, d in nearby[:3]:
            lbl = QLabel(f"  •  {other['name']} (distance: {d:.1f})")
            lbl.setStyleSheet(f"color: {other['color']}; font-size: 12px;")
            layout.addWidget(lbl)

        layout.addSpacing(15)
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton { background-color: #0f3460; color: white; border: none;
                          border-radius: 6px; padding: 10px 30px; font-size: 14px; }
            QPushButton:hover { background-color: #1a4a80; }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    @staticmethod
    def _section(text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #e94560; margin-top: 10px;")
        return lbl


# ============================================================================
# PAGES
# ============================================================================

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("🏛️  Political Ideologies Explorer")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #e94560;")
        layout.addWidget(header)

        subtitle = QLabel(
            "Understand the political spectrum — from left to right, authoritarian to libertarian.\n"
            "Explore ideologies, take the compass quiz, and compare political philosophies side by side."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #aaa; font-size: 14px; line-height: 1.6;")
        layout.addWidget(subtitle)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)
        stats_data = [
            ("📚", f"{len(IDEOLOGIES)} Ideologies", "Major political philosophies covered"),
            ("❓", f"{len(QUIZ_QUESTIONS)} Questions", "Compass assessment with dual-axis scoring"),
            ("📖", f"{len(GLOSSARY)} Terms", "Essential political science vocabulary"),
        ]
        for icon, title, desc in stats_data:
            card = QFrame()
            card.setStyleSheet("QFrame { background-color: #16213e; border-radius: 10px; padding: 14px; }")
            cl = QVBoxLayout(card)
            cl.setSpacing(4)
            l1 = QLabel(icon); l1.setStyleSheet("font-size: 26px;")
            l2 = QLabel(title); l2.setStyleSheet("font-size: 15px; font-weight: bold; color: #eee;")
            l3 = QLabel(desc); l3.setStyleSheet("color: #999; font-size: 11px;")
            cl.addWidget(l1); cl.addWidget(l2); cl.addWidget(l3)
            stats_row.addWidget(card)
        layout.addLayout(stats_row)

        # Compass explanation
        section = QLabel("The Political Compass")
        section.setStyleSheet("font-size: 18px; font-weight: bold; color: #e94560; margin-top: 10px;")
        layout.addWidget(section)

        compass_text = QLabel(
            "The political compass is a two-dimensional model that maps ideologies along two independent axes:\n\n"
            "  •  Economic (Left ↔ Right): Collective/state-controlled economy (left) vs. free-market/individual economy (right)\n"
            "  •  Social (Authoritarian ↔ Libertarian): State control of personal life (top) vs. maximum personal freedom (bottom)\n\n"
            "This model reveals that ideologies can share economic positions while differing sharply on social freedom "
            "— nuance that a simple left–right line cannot capture."
        )
        compass_text.setWordWrap(True)
        compass_text.setStyleSheet("color: #bbb; font-size: 12px; line-height: 1.6;")
        layout.addWidget(compass_text)

        # Compass chart
        compass = CompassWidget()
        compass.setFixedHeight(380)
        layout.addWidget(compass)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)


class ExplorerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("📚  Ideology Explorer")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #e94560;")
        layout.addWidget(header)

        desc = QLabel("Click on any card to see a full description, key principles, and notable thinkers.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(desc)

        # Filter bar
        fl = QHBoxLayout()
        filter_label = QLabel("Filter by quadrant:")
        filter_label.setStyleSheet("color: #ccc; font-size: 12px;")
        fl.addWidget(filter_label)
        self.filter = QComboBox()
        self.filter.addItems(["All", "Authoritarian Left", "Authoritarian Right",
                               "Libertarian Left", "Libertarian Right"])
        self.filter.setStyleSheet("""
            QComboBox { background-color: #16213e; color: #ddd; border: 1px solid #333;
                        border-radius: 5px; padding: 6px 12px; font-size: 12px; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #16213e; color: #ddd;
                                          selection-background-color: #0f3460; }
        """)
        self.filter.currentTextChanged.connect(self._rebuild)
        fl.addWidget(self.filter)
        fl.addStretch()
        layout.addLayout(fl)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(12)
        self.scroll.setWidget(self.grid_widget)
        layout.addWidget(self.scroll)
        self._rebuild("All")

    def _rebuild(self, filter_text):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        row, col = 0, 0
        for ideo in IDEOLOGIES:
            if filter_text != "All":
                e, s = ideo["econ"], ideo["social"]
                if filter_text == "Authoritarian Left" and not (e < 0 and s > 0):
                    continue
                if filter_text == "Authoritarian Right" and not (e >= 0 and s > 0):
                    continue
                if filter_text == "Libertarian Left" and not (e < 0 and s <= 0):
                    continue
                if filter_text == "Libertarian Right" and not (e >= 0 and s <= 0):
                    continue
            card = ClickableCard(ideo)
            card.clicked.connect(self._open_detail)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def _open_detail(self, ideo):
        IdeologyDetailDialog(ideo, self).exec()


class QuizPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_q = 0
        self.answers = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        outer.addWidget(self.scroll)
        self._show_welcome()

    def _set_content(self, widget):
        old = self.scroll.takeWidget()
        if old:
            old.deleteLater()
        self.scroll.setWidget(widget)

    def _show_welcome(self):
        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setSpacing(20)
        lo.setContentsMargins(50, 50, 50, 50)
        lo.setAlignment(Qt.AlignCenter)

        hdr = QLabel("🧭  Political Compass Quiz")
        hdr.setAlignment(Qt.AlignCenter)
        hdr.setStyleSheet("font-size: 26px; font-weight: bold; color: #e94560;")
        lo.addWidget(hdr)

        body = QLabel(
            "Answer 25 questions to discover where you fall on the political compass.\n\n"
            "Rate each statement from Strongly Disagree to Strongly Agree.\n"
            "There are no right or wrong answers — be honest for the most accurate result."
        )
        body.setAlignment(Qt.AlignCenter)
        body.setWordWrap(True)
        body.setStyleSheet("color: #aaa; font-size: 14px; line-height: 1.7;")
        lo.addWidget(body)

        btn = QPushButton("🎯  Start Quiz")
        btn.setFixedSize(220, 55)
        btn.setStyleSheet("""
            QPushButton { background-color: #e94560; color: white; border: none;
                          border-radius: 10px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #ff5a75; }
        """)
        btn.clicked.connect(self._start)
        lo.addWidget(btn, alignment=Qt.AlignCenter)
        lo.addStretch()
        self._set_content(w)

    def _start(self):
        self.current_q = 0
        self.answers = []
        self._show_question()

    def _show_question(self):
        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setSpacing(16)
        lo.setContentsMargins(40, 30, 40, 30)

        bar = QProgressBar()
        bar.setRange(0, len(QUIZ_QUESTIONS))
        bar.setValue(self.current_q)
        bar.setFormat(f"Question {self.current_q + 1} of {len(QUIZ_QUESTIONS)}")
        bar.setStyleSheet("""
            QProgressBar { background-color: #16213e; border: none; border-radius: 8px;
                           height: 26px; color: white; text-align: center; font-size: 11px; }
            QProgressBar::chunk { background-color: #e94560; border-radius: 8px; }
        """)
        lo.addWidget(bar)

        qnum = QLabel(f"Question {self.current_q + 1}")
        qnum.setStyleSheet("color: #e94560; font-size: 12px; font-weight: bold;")
        lo.addWidget(qnum)

        qtext = QLabel(QUIZ_QUESTIONS[self.current_q]["text"])
        qtext.setWordWrap(True)
        qtext.setStyleSheet("color: #eee; font-size: 17px; line-height: 1.5; margin: 8px 0;")
        lo.addWidget(qtext)

        options = [
            ("Strongly Disagree", -2, "#c0392b"),
            ("Disagree", -1, "#e74c3c"),
            ("Neutral", 0, "#7f8c8d"),
            ("Agree", 1, "#27ae60"),
            ("Strongly Agree", 2, "#1e8449"),
        ]
        self.btn_group = QButtonGroup(self)

        for text, value, color in options:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setProperty("answer_value", value)
            btn.setFixedHeight(44)
            btn.setStyleSheet(f"""
                QPushButton {{ background-color: #16213e; color: #ccc; border: 2px solid #333;
                    border-radius: 8px; font-size: 13px; text-align: left; padding-left: 20px; }}
                QPushButton:hover {{ border-color: {color}; background-color: #1e2d42; }}
                QPushButton:checked {{ background-color: {color}44; border-color: {color};
                    color: white; font-weight: bold; }}
            """)
            self.btn_group.addButton(btn)
            lo.addWidget(btn)

        if self.current_q < len(self.answers):
            val = self.answers[self.current_q]
            for btn in self.btn_group.buttons():
                if btn.property("answer_value") == val:
                    btn.setChecked(True)
                    break

        nav = QHBoxLayout()
        if self.current_q > 0:
            prev = QPushButton("← Previous")
            prev.setStyleSheet("""
                QPushButton { background-color: #333; color: #ccc; border: none;
                    border-radius: 6px; padding: 10px 20px; font-size: 13px; }
                QPushButton:hover { background-color: #444; }
            """)
            prev.clicked.connect(self._prev)
            nav.addWidget(prev)
        nav.addStretch()

        next_text = "Next →" if self.current_q < len(QUIZ_QUESTIONS) - 1 else "🎯 See Results"
        next_btn = QPushButton(next_text)
        next_btn.setStyleSheet("""
            QPushButton { background-color: #e94560; color: white; border: none;
                border-radius: 6px; padding: 10px 24px; font-size: 13px; font-weight: bold; }
            QPushButton:hover { background-color: #ff5a75; }
        """)
        next_btn.clicked.connect(self._next)
        nav.addWidget(next_btn)
        lo.addLayout(nav)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
        lo.addWidget(self.warning_label)

        lo.addStretch()
        self._set_content(w)

    def _prev(self):
        if self.current_q > 0:
            self.current_q -= 1
            self._show_question()

    def _next(self):
        selected = self.btn_group.checkedButton()
        if not selected:
            if self.warning_label:
                self.warning_label.setText("⚠  Please select an answer before continuing.")
            return
        value = selected.property("answer_value")

        if self.current_q < len(self.answers):
            self.answers[self.current_q] = value
        else:
            self.answers.append(value)

        self.current_q += 1
        if self.current_q >= len(QUIZ_QUESTIONS):
            self._show_results()
        else:
            self._show_question()

    def _show_results(self):
        econ_score = 0.0
        social_score = 0.0
        for i, ans in enumerate(self.answers):
            q = QUIZ_QUESTIONS[i]
            econ_score += ans * q["econ"]
            social_score += ans * q["social"]

        max_possible = sum(abs(q["econ"]) * 2 for q in QUIZ_QUESTIONS)
        if max_possible == 0:
            max_possible = 1
        econ_norm = (econ_score / max_possible) * 10.0
        social_norm = (social_score / max_possible) * 10.0
        econ_norm = max(-10.0, min(10.0, econ_norm))
        social_norm = max(-10.0, min(10.0, social_norm))

        best = None
        best_dist = float("inf")
        max_d = 20 * math.sqrt(2)
        match_percentages = {}
        for ideo in IDEOLOGIES:
            d = math.hypot(ideo["econ"] - econ_norm, ideo["social"] - social_norm)
            match_percentages[ideo["name"]] = max(0, (1.0 - d / max_d) * 100)
            if d < best_dist:
                best_dist = d
                best = ideo

        quadrant = "Libertarian Left" if econ_norm < 0 and social_norm < 0 else \
                   "Libertarian Right" if econ_norm >= 0 and social_norm < 0 else \
                   "Authoritarian Left" if econ_norm < 0 else "Authoritarian Right"

        w = QWidget()
        lo = QVBoxLayout(w)
        lo.setSpacing(14)
        lo.setContentsMargins(40, 30, 40, 30)

        hdr = QLabel("🎯  Your Results")
        hdr.setAlignment(Qt.AlignCenter)
        hdr.setStyleSheet("font-size: 24px; font-weight: bold; color: #e94560;")
        lo.addWidget(hdr)

        # Two charts side by side
        charts_row = QHBoxLayout()
        compass = CompassWidget()
        compass.set_user_position(econ_norm, social_norm)
        compass.setMinimumHeight(350)
        charts_row.addWidget(compass)

        radar = RadarChartWidget()
        radar.set_data(econ_norm, social_norm)
        radar.setMinimumHeight(350)
        charts_row.addWidget(radar)
        lo.addLayout(charts_row)

        # Scores frame
        scores_frame = QFrame()
        scores_frame.setStyleSheet("QFrame { background-color: #16213e; border-radius: 10px; padding: 15px; }")
        sl = QVBoxLayout(scores_frame)
        sl.setSpacing(8)

        econ_label = QLabel(f"Economic Axis:  {econ_norm:+.1f}  ({'Right' if econ_norm >= 0 else 'Left'})")
        econ_label.setStyleSheet("color: #eee; font-size: 14px; font-weight: bold;")
        sl.addWidget(econ_label)

        econ_bar = QProgressBar()
        econ_bar.setRange(-100, 100)
        econ_bar.setValue(int(econ_norm * 10))
        econ_bar.setFormat("")
        econ_bar.setFixedHeight(14)
        econ_bar.setStyleSheet("""
            QProgressBar { background-color: #333; border: none; border-radius: 7px; }
            QProgressBar::chunk { background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:0.5 #7f8c8d, stop:1 #3498db);
                border-radius: 7px; }
        """)
        sl.addWidget(econ_bar)

        soc_label = QLabel(f"Social Axis:  {social_norm:+.1f}  ({'Authoritarian' if social_norm >= 0 else 'Libertarian'})")
        soc_label.setStyleSheet("color: #eee; font-size: 14px; font-weight: bold;")
        sl.addWidget(soc_label)

        soc_bar = QProgressBar()
        soc_bar.setRange(-100, 100)
        soc_bar.setValue(int(social_norm * 10))
        soc_bar.setFormat("")
        soc_bar.setFixedHeight(14)
        soc_bar.setStyleSheet("""
            QProgressBar { background-color: #333; border: none; border-radius: 7px; }
            QProgressBar::chunk { background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0, stop:0 #2ecc71, stop:0.5 #7f8c8d, stop:1 #9b59b6);
                border-radius: 7px; }
        """)
        sl.addWidget(soc_bar)
        lo.addWidget(scores_frame)

        # Top 5 matches
        top5 = sorted(match_percentages.items(), key=lambda x: -x[1])[:5]
        match_frame = QFrame()
        match_frame.setStyleSheet("QFrame { background-color: #1e2a3a; border-radius: 12px; padding: 16px; }")
        ml = QVBoxLayout(match_frame)
        ml.setSpacing(8)

        ml_title = QLabel("📊  Ideology Match Scores")
        ml_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e94560;")
        ml.addWidget(ml_title)

        for rank, (name, pct) in enumerate(top5, 1):
            ideo = next(i for i in IDEOLOGIES if i["name"] == name)
            row = QHBoxLayout()

            rank_lbl = QLabel(f"#{rank}")
            rank_lbl.setFixedWidth(25)
            rank_lbl.setStyleSheet("color: #888; font-size: 12px; font-weight: bold;")
            row.addWidget(rank_lbl)

            name_lbl = QLabel(f"● {name}")
            name_lbl.setStyleSheet(f"color: {ideo['color']}; font-size: 13px; font-weight: bold;")
            name_lbl.setFixedWidth(160)
            row.addWidget(name_lbl)

            bar_frame = QFrame()
            bar_frame.setFixedHeight(18)
            bar_frame.setStyleSheet("background-color: #0a0a1a; border-radius: 9px;")
            bar_layout = QHBoxLayout(bar_frame)
            bar_layout.setContentsMargins(2, 2, 2, 2)
            bar_layout.setSpacing(0)

            fill = QFrame()
            fill_w = max(4, int(pct * 2.5))
            fill.setFixedWidth(fill_w)
            fill.setStyleSheet(f"background-color: {ideo['color']}; border-radius: 7px;")
            bar_layout.addWidget(fill)
            bar_layout.addStretch()
            row.addWidget(bar_frame, stretch=1)

            pct_lbl = QLabel(f"{pct:.0f}%")
            pct_lbl.setFixedWidth(45)
            pct_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            pct_lbl.setStyleSheet("color: #ccc; font-size: 12px; font-weight: bold;")
            row.addWidget(pct_lbl)

            ml.addLayout(row)
        lo.addWidget(match_frame)

        # Closest match card
        match_card = QFrame()
        match_card.setStyleSheet(f"""
            QFrame {{ background-color: #1e2a3a; border: 2px solid {best['color']}66;
                      border-radius: 12px; padding: 18px; }}
        """)
        mcl = QVBoxLayout(match_card)
        mcl.setSpacing(6)

        t = QLabel(f"🏷️  Closest Match:  {best['name']}")
        t.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {best['color']};")
        mcl.addWidget(t)

        q_lbl = QLabel(f"Quadrant:  {quadrant}")
        q_lbl.setStyleSheet("color: #ccc; font-size: 14px;")
        mcl.addWidget(q_lbl)

        s_lbl = QLabel(best["summary"])
        s_lbl.setWordWrap(True)
        s_lbl.setStyleSheet("color: #bbb; font-size: 12px; line-height: 1.5;")
        mcl.addWidget(s_lbl)

        detail_btn = QPushButton(f"📖  Read more about {best['name']}")
        detail_btn.setStyleSheet("""
            QPushButton { background-color: #0f3460; color: white; border: none;
                border-radius: 6px; padding: 8px 16px; font-size: 12px; }
            QPushButton:hover { background-color: #1a4a80; }
        """)
        detail_btn.clicked.connect(lambda: IdeologyDetailDialog(best, self).exec())
        mcl.addWidget(detail_btn)
        lo.addWidget(match_card)

        # Buttons Row
        btn_row = QHBoxLayout()
        
        retake = QPushButton("🔄  Retake Quiz")
        retake.setFixedHeight(48)
        retake.setStyleSheet("""
            QPushButton { background-color: #e94560; color: white; border: none;
                border-radius: 8px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #ff5a75; }
        """)
        retake.clicked.connect(self._show_welcome)
        btn_row.addWidget(retake)

        export_btn = QPushButton("💾  Export Results")
        export_btn.setFixedHeight(48)
        export_btn.setStyleSheet("""
            QPushButton { background-color: #16213e; color: #ccc; border: 1px solid #444;
                border-radius: 8px; font-size: 13px; font-weight: bold; }
            QPushButton:hover { background-color: #1e2d42; border-color: #e94560; }
        """)
        export_btn.clicked.connect(
            lambda: self._export_results(econ_norm, social_norm, match_percentages)
        )
        btn_row.addWidget(export_btn)
        
        lo.addLayout(btn_row)
        lo.addStretch()
        self._set_content(w)

    def _export_results(self, econ_norm, social_norm, match_percentages):
        quadrant = "Libertarian Left" if econ_norm < 0 and social_norm < 0 else \
                   "Libertarian Right" if econ_norm >= 0 and social_norm < 0 else \
                   "Authoritarian Left" if econ_norm < 0 else "Authoritarian Right"

        sorted_matches = sorted(match_percentages.items(), key=lambda x: -x[1])

        text = "=" * 60 + "\n"
        text += "  POLITICAL COMPASS QUIZ — RESULTS\n"
        text += "=" * 60 + "\n\n"
        text += f"  Economic Axis:  {econ_norm:+.1f}  ({'Right' if econ_norm >= 0 else 'Left'})\n"
        text += f"  Social Axis:    {social_norm:+.1f}  ({'Authoritarian' if social_norm >= 0 else 'Libertarian'})\n"
        text += f"  Quadrant:       {quadrant}\n\n"

        text += "-" * 60 + "\n"
        text += "  IDEOLOGY MATCH SCORES\n"
        text += "-" * 60 + "\n"
        for name, pct in sorted_matches:
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            text += f"  {name:<20s} {bar} {pct:5.1f}%\n"

        text += "\n" + "-" * 60 + "\n"
        text += "  YOUR ANSWERS\n"
        text += "-" * 60 + "\n"
        for i, ans in enumerate(self.answers):
            labels = {-2: "Strongly Disagree", -1: "Disagree", 0: "Neutral",
                      1: "Agree", 2: "Strongly Agree"}
            text += f"  Q{i+1:2d}. {QUIZ_QUESTIONS[i]['text']}\n"
            text += f"      -> {labels.get(ans, 'N/A')}\n\n"

        text += "=" * 60 + "\n"

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "political_compass_results.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)


class ComparePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(30, 30, 30, 30)

        hdr = QLabel("⚖️  Compare Ideologies")
        hdr.setStyleSheet("font-size: 24px; font-weight: bold; color: #e94560;")
        layout.addWidget(hdr)

        desc = QLabel("Select two ideologies to compare their principles, thinkers, and compass positions side by side.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(desc)

        sel = QHBoxLayout()
        names = [i["name"] for i in IDEOLOGIES]

        self.combo_a = QComboBox()
        self.combo_a.addItems(names)
        self.combo_a.setCurrentIndex(0)
        self._style_combo(self.combo_a)
        sel.addWidget(self.combo_a)

        vs = QLabel("VS")
        vs.setAlignment(Qt.AlignCenter)
        vs.setStyleSheet("color: #e94560; font-size: 20px; font-weight: bold;")
        sel.addWidget(vs)

        self.combo_b = QComboBox()
        self.combo_b.addItems(names)
        self.combo_b.setCurrentIndex(7)
        self._style_combo(self.combo_b)
        sel.addWidget(self.combo_b)

        compare_btn = QPushButton("Compare")
        compare_btn.setStyleSheet("""
            QPushButton { background-color: #e94560; color: white; border: none;
                border-radius: 6px; padding: 10px 24px; font-size: 13px; font-weight: bold; }
            QPushButton:hover { background-color: #ff5a75; }
        """)
        compare_btn.clicked.connect(self._update)
        sel.addWidget(compare_btn)
        layout.addLayout(sel)

        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.result_widget = QWidget()
        self.result_layout = QHBoxLayout(self.result_widget)
        self.result_scroll.setWidget(self.result_widget)
        layout.addWidget(self.result_scroll, stretch=1)

        self._update()

    @staticmethod
    def _style_combo(cb):
        cb.setStyleSheet("""
            QComboBox { background-color: #16213e; color: #ddd; border: 1px solid #444;
                        border-radius: 6px; padding: 8px 14px; font-size: 13px; min-width: 160px; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #16213e; color: #ddd;
                                          selection-background-color: #0f3460; }
        """)

    def _build_card(self, ideo):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{ background-color: #16213e; border: 2px solid {ideo['color']}55;
                      border-radius: 12px; padding: 14px; }}
        """)
        lo = QVBoxLayout(card)
        lo.setSpacing(8)

        title = QLabel(ideo["name"])
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {ideo['color']};")
        title.setAlignment(Qt.AlignCenter)
        lo.addWidget(title)

        origin = QLabel(f"Origin: {ideo['origin']}")
        origin.setStyleSheet("color: #999; font-size: 11px;")
        origin.setAlignment(Qt.AlignCenter)
        lo.addWidget(origin)

        lo.addWidget(self._sep())

        pos = QLabel(f"📍  Economic: {ideo['econ']:+d}   |   Social: {ideo['social']:+d}")
        pos.setStyleSheet("color: #ccc; font-size: 12px;")
        pos.setAlignment(Qt.AlignCenter)
        lo.addWidget(pos)

        lo.addWidget(self._sep())

        sec1 = QLabel("Key Principles")
        sec1.setStyleSheet("font-size: 13px; font-weight: bold; color: #e94560;")
        lo.addWidget(sec1)
        for pr in ideo["principles"]:
            lbl = QLabel(f"  •  {pr}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #bbb; font-size: 11px;")
            lo.addWidget(lbl)

        lo.addWidget(self._sep())

        sec2 = QLabel("Notable Thinkers")
        sec2.setStyleSheet("font-size: 13px; font-weight: bold; color: #e94560;")
        lo.addWidget(sec2)
        for th in ideo["thinkers"]:
            lbl = QLabel(f"  •  {th}")
            lbl.setStyleSheet("color: #bbb; font-size: 11px;")
            lo.addWidget(lbl)

        lo.addStretch()
        return card

    @staticmethod
    def _sep():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #333;")
        return line

    def _update(self):
        idx_a = self.combo_a.currentIndex()
        idx_b = self.combo_b.currentIndex()
        ideo_a = IDEOLOGIES[idx_a]
        ideo_b = IDEOLOGIES[idx_b]

        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.result_layout.addWidget(self._build_card(ideo_a))
        self.result_layout.addWidget(self._build_card(ideo_b))


class TimelinePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 30, 40, 30)

        hdr = QLabel("📅  Historical Timeline")
        hdr.setStyleSheet("font-size: 24px; font-weight: bold; color: #e94560;")
        layout.addWidget(hdr)

        desc = QLabel("Trace the evolution of political ideologies from the Magna Carta to the present day.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #aaa; font-size: 13px; margin-bottom: 20px;")
        layout.addWidget(desc)

        for i, event in enumerate(TIMELINE_EVENTS):
            row = QHBoxLayout()
            row.setSpacing(16)

            year_label = QLabel(str(event["year"]))
            year_label.setFixedWidth(60)
            year_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            year_label.setStyleSheet(f"color: {event['color']}; font-size: 16px; font-weight: bold;")
            row.addWidget(year_label)

            connector = QVBoxLayout()
            connector.setSpacing(0)

            dot = QLabel("●")
            dot.setFixedWidth(20)
            dot.setAlignment(Qt.AlignCenter)
            dot.setStyleSheet(f"color: {event['color']}; font-size: 14px;")
            connector.addWidget(dot)

            if i < len(TIMELINE_EVENTS) - 1:
                line = QFrame()
                line.setFixedWidth(2)
                line.setMinimumHeight(30)
                line.setStyleSheet("background-color: #333;")
                connector.addWidget(line)

            row.addLayout(connector)

            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{ background-color: #16213e; border-left: 3px solid {event['color']};
                          border-radius: 0 8px 8px 0; padding: 12px 16px; }}
            """)
            cl = QVBoxLayout(card)
            cl.setSpacing(4)

            title = QLabel(event["title"])
            title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {event['color']};")
            cl.addWidget(title)

            desc_text = QLabel(event["desc"])
            desc_text.setWordWrap(True)
            desc_text.setStyleSheet("color: #bbb; font-size: 11px; line-height: 1.5;")
            cl.addWidget(desc_text)

            row.addWidget(card, stretch=1)
            layout.addLayout(row)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)


class GlossaryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        lo = QVBoxLayout(content)
        lo.setSpacing(12)
        lo.setContentsMargins(30, 30, 30, 30)

        hdr = QLabel("📖  Glossary of Key Terms")
        hdr.setStyleSheet("font-size: 24px; font-weight: bold; color: #e94560;")
        lo.addWidget(hdr)

        desc = QLabel("Essential political science concepts and their definitions.")
        desc.setStyleSheet("color: #aaa; font-size: 13px;")
        lo.addWidget(desc)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Search terms...")
        self.search.setStyleSheet("""
            QLineEdit { background-color: #16213e; color: #ddd; border: 1px solid #444;
                        border-radius: 8px; padding: 10px 16px; font-size: 13px; }
            QLineEdit:focus { border-color: #e94560; }
        """)
        self.search.textChanged.connect(self._filter)
        lo.addWidget(self.search)

        self.terms_container = QVBoxLayout()
        lo.addLayout(self.terms_container)

        self.term_widgets = []
        for term, definition in sorted(GLOSSARY.items()):
            card = QFrame()
            card.setStyleSheet("QFrame { background-color: #16213e; border-radius: 8px; padding: 12px; }")
            cl = QVBoxLayout(card)
            cl.setSpacing(4)

            t = QLabel(term)
            t.setStyleSheet("font-size: 14px; font-weight: bold; color: #e94560;")
            cl.addWidget(t)

            d = QLabel(definition)
            d.setWordWrap(True)
            d.setStyleSheet("color: #bbb; font-size: 12px; line-height: 1.5;")
            cl.addWidget(d)

            self.terms_container.addWidget(card)
            self.term_widgets.append((term.lower(), card))

        lo.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

    def _filter(self, text):
        search = text.strip().lower()
        for term_lower, card in self.term_widgets:
            card.setVisible(search == "" or search in term_lower)


# ============================================================================
# MAIN WINDOW
# ============================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Political Ideologies Explorer")
        self.setMinimumSize(900, 650)
        self.resize(1100, 750)
        self.setStyleSheet("""
            QMainWindow { background-color: #0f0f23; }
            QWidget { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Nav bar
        nav = QFrame()
        nav.setFixedHeight(56)
        nav.setStyleSheet("""
            QFrame { background-color: #16213e; border-bottom: 1px solid #1a1a3e; }
            QPushButton { background-color: transparent; color: #8899aa; border: none;
                          border-radius: 6px; padding: 8px 16px; font-size: 13px; font-weight: bold; }
            QPushButton:hover { color: #e94560; background-color: #1a2a4a; }
            QPushButton:checked { color: #e94560; background-color: #0f346066; }
        """)
        nav_layout = QHBoxLayout(nav)
        nav_layout.setContentsMargins(20, 0, 20, 0)

        brand = QLabel("🏛️ PolSci")
        brand.setStyleSheet("color: #e94560; font-size: 16px; font-weight: bold; margin-right: 20px;")
        nav_layout.addWidget(brand)

        self.nav_buttons = []
        pages = [
            ("🏠 Home", "home"),
            ("📚 Explorer", "explorer"),
            ("🧭 Quiz", "quiz"),
            ("⚖️ Compare", "compare"),
            ("📅 Timeline", "timeline"),
            ("📖 Glossary", "glossary"),
        ]
        for label, key in pages:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("page_key", key)
            btn.clicked.connect(lambda checked, k=key: self._switch(k))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        nav_layout.addStretch()
        self.nav_buttons[0].setChecked(True)

        main_layout.addWidget(nav)

        # Stacked pages
        self.stack = QStackedWidget()
        self.pages = {
            "home": HomePage(),
            "explorer": ExplorerPage(),
            "quiz": QuizPage(),
            "compare": ComparePage(),
            "timeline": TimelinePage(),
            "glossary": GlossaryPage(),
        }
        for key in ["home", "explorer", "quiz", "compare", "timeline", "glossary"]:
            self.stack.addWidget(self.pages[key])

        main_layout.addWidget(self.stack)

    def _switch(self, key):
        idx = list(self.pages.keys()).index(key)
        self.stack.setCurrentIndex(idx)
        for btn in self.nav_buttons:
            btn.setChecked(btn.property("page_key") == key)


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0f0f23"))
    palette.setColor(QPalette.WindowText, QColor("#dddddd"))
    palette.setColor(QPalette.Base, QColor("#16213e"))
    palette.setColor(QPalette.AlternateBase, QColor("#1a2744"))
    palette.setColor(QPalette.ToolTipBase, QColor("#16213e"))
    palette.setColor(QPalette.ToolTipText, QColor("#dddddd"))
    palette.setColor(QPalette.Text, QColor("#dddddd"))
    palette.setColor(QPalette.Button, QColor("#16213e"))
    palette.setColor(QPalette.ButtonText, QColor("#dddddd"))
    palette.setColor(QPalette.BrightText, QColor("#e94560"))
    palette.setColor(QPalette.Link, QColor("#e94560"))
    palette.setColor(QPalette.Highlight, QColor("#0f3460"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()