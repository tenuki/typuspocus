# -*- coding: iso-8859-1 -*-
claves = """
nombre
audiencia
objeto
hechizo
historyintro
historygood
historybad
titulo
params
""".strip().split("\n")

textosNiveles = [
    (
        "Teatro prestado",
        "Pocos, variados",
        "Un conejo",
        "Hocus pocus, disappear now.",
"""Cast the spell 
as fast and accurately as you can. 

You can backspace and fix 
your mistakes.""",

        """Great! You receive an offer to perform in the "Paris Opera".""",
        "You are not even worthy of this demo level.",
        "Mandrake",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),

    (
        "Opera",
        "Gente vestida bien",
        "La mascara del fantasma de la opera",
        "evanesco simulatio, phantasma spectaculum. initium capere.",
"""Dissapear the Phantom's mask, 

that will embarass him and 
make him leave.""",
        "Your act was great! You are invited to perform the Halftime show at the local basquetball finals.",
        "You blew it, your father disinherited you. You get a job coding ruby on rails.",
        "Gandalf",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),


    (
        "Magic arena",
        "Jugadores de basquet o deportistas",
        "Zapatillas grandes.",
        "luckyus calceus sneakerus, evanesco consagrus, valius playerus, propugnator turma championus.",
"""The locals are loosing by 12,
 
you must dissapear the 

visitor's MVP lucky sneakers.""",
        "Thanks to your help the locals win and you get invited to do your trick at the after party.",
        "An Angry mob of the local fans chases you around the stadium.",
        "Harry Potter",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),


    (
        "Fiesta musical",
        "Hip-hoperos o darkies",
        "Alcohol, drogas, hacer un mix",
        "sexus drugus rockanrolus, captivus crowdimus yowasaaap. cops and hardcopy marihuanus boozelion, cocuchus chuchu fuchu.",
"""You were supposed to dissapear a 
milli vanilli cd, 
instead you must vanish the 
drugs to hide them 
from the cops.""",
        "You got away clean, and kept a lot of famous people out of jail. You are going to Las Vegas now!!",
        "You go to jail charged with drug possession. And become RAUL's new girlfriend.",
        "David Copperfield",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),


    (
        "Las Vegas",
        "Gente adinerada",
        "papeles y documentos",
        "factus taxus nuLus, nilun actin, evaDus fiscus IRSus, whySaw Elvis Bellagium 11 ocean's cardus impustum disapiros ipsofactum.",
        "You get to Las Vegas to perform in a Casino, but the owners want to take advantage of your power to evade taxes.",
        "The IRS wants you for beeing an accesory to tax evasion. They send you Africa where they'll never find you",
        "Your act was a total failure, you got wasted and lost all your money playing craps.",
        "Orko",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),


    (
        "Black magic",
        "Africanitos de la tribu",
        "Un muricélago, o algún animal raro",
        "Batsimus chicaka aFrIcuN triBuson, ill chikakun medicor, nigrum. comedo. crudus...pain cooking Shutlewor meellon cHuNgo.",
        "You go to live with a tribe in africa,  they find out you are a wizard and want you to heal their ill sacred animal",
        "You dissapeared the sacred animal. The angry natives start chasing you around the jungle.",
        "The natives made a tasty casserole out of you.",
        "Merlyn",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),

    (
        "Tatooine",
        "Robots de star wars",
        "Aspiradora loca",
        "Arturitum Vacuumcleanerum Ev4niscum c3p0 venusiun rescusum grossum ph1ll1ps, disapirum spacious robotitus shakulus.",
        "While running away from the natives, a spaceship abdu^H^H^H^Hrescues you. The venusians ask you to help them vanish a hitchhiker.",
        "Since you were so helpfull, the venusians send you back to earth in an individual spaceship.",
        "Because you were unwilling to cooperate, the venusians performed a 'light saber anal probing' on you.",
        "Harry Houdini",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),

    (
        "Area 51",
        "Marcianitos y men in black",
        "un marcianito de roswell",
        "Marcianus 51area alf rosswellin didosong untilyourestingherewithme evanisum marcianus y guarda que viene molderrr.",
        "Your ship was running a pirated OS and crashed in new mexico. The FBI captures you and asks you to dissapear some evidence of the alien landings.",
        "Now that the evidence exists only on your memory, the FBI makes sure you won't talk by putting a cap in your head",
        "You couldn't do it. But you'll have a lot of time to practice since you are never leaving area 51",
        "Skeletor",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),

    (
        "Graveyard",
        "Esqueletos",
        "Estatuilla de Anubis",
        "vaderetrum satinus anubisun chungus, transformix this decayed form to Mumm-ra the Everliving and the puwur of christus will savius vox. ",
        "Ok, you died, and went to hell, you can escape to heaven by dissapearing Anubis. All the dead gather around to watch...",
        "You did it!!! Now you go to heaven, that happy place we all dream about as kids, that place where men and women love each other. ",
        "You stay in hell. At least you won't have problems finding a lawyer if you ever come to need one.",
        "Mumm-Ra",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),


    (
        "EL LUGAR FELIZ",
        "Todos desnudos",
        "CUZCO la cabra",
        "caelum CUZCUS 13 paradisiun, revivisco animalis playboyus housus, pornus sexus gross klunx workus my clunk essta noshi inbolus minusem. miau miau.",
        "Here we are, it's beautiful, everything that dissapears here goes back to earth, so you are going to revive a lovely goat now!",
        "Congratulations! You fullfilled your destiny as a magician!",
        "Mmm... Too bad you couldn't do it, but hey, a horde of naked angels offers to console you!!",
        "Lord Zedd",
        dict(tiempo_por_caracter=0.35, preferencia_precision=0.1)
    ),
]

class Niveles:
    def __init__(self, keys, values):
        for k,v in zip(keys, values):
            setattr(self, k, v)

niveles = [ Niveles(claves, values) for values in textosNiveles ]

if __name__ == "__main__":
    for n in niveles:
        print dir(n)
