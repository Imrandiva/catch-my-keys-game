<h1>Dokumentation av protokollet</h1>
<h2>Bygg en klient med hjälp av detta protokoll</h2>

<h3>Illustrerande tillståndsdiagram</h3>
Detta tillståndsdiagram hjälper dig att visualisera den datan som skickas
mellan servern och klienterna; hur det går till och det som skickas fram och tillbaka.


- Kolla state_diagram.png 


<h3> Data som skickas mellan klient och server</h3>
Det som skickas fram och tillbaka mellan servern och klienterna är en JSON fil med information om den andra spelarens position, dess spelar-id, nycklar som finns tillgängliga på planen och nycklar som ska försvinna från båda spelarna ifall dess livlängd har gått ut eller om en av spelarna har plockat upp denna. Klienten uppdaterar denna data som skickas från servern med ny information som skickar tillbaks till servern som återigen uppdaterar den andra spelaren med den nya datan och vice versa. 

<h3> Detaljer om JSON filen </h3>

<code>

    # Kod från serverfilen
    info1 = {
        "player-id": 0,
        "player-x-pos": 50,
        "player-y-pos": 100,
        "player-keys": 0,
        "keys": [],
        "keysToRemove": []
    }
</code>

Detta är ett exempel från servern för vad som skickas, med andra ord, all nödvändig info 
som klienten behöver för att konstruera exempel objekt för nycklar, eller spelarobjekt. Alltså
sker parsningen i klienten, och det är endast denna json sträng som skickas mellan servern och klienten.
Teckenkodningen bör vara utf-8.

<h3>Network-filen - Bryggan mellan servern och klienterna</h3>

Det är i network.py som vi initierar kopplingen mellan servern och olika klienter. Det är här vi kopplar samman till hostens IP-adress. 
Det är i Networks send_data() funktion som klienten kan skicka uppdaterad data till servern.
Det är här som klienten kan koppla samman med servern via Networks start_connection() funktion. 

Använd dessa funktioner som finns i network.py för att koppla samman din klient med servern. 

Serverkod inspirerat av TechwithTims tutorial för hur man använder Python Sockets: https://www.techwithtim.net/tutorials/socket-programming/
