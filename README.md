# NBA Match Analyzer

App gratuita in italiano per consultare i risultati della stagione NBA corrente e analizzare forma squadra e statistiche individuali.

## Avvio su Windows

1. Installa Python 3 dal sito ufficiale e durante l'installazione seleziona **Add Python to PATH**.
2. Scarica il repository con **Code → Download ZIP** ed estrailo.
3. Apri la cartella `nba-match-analyzer`.
4. Clicca la barra del percorso in alto, scrivi `powershell` e premi Invio.
5. Nella finestra che si apre, esegui questi comandi uno alla volta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Quando appare `http://localhost:8501`, apri quell'indirizzo nel browser. Per fermare l'app torna alla finestra PowerShell e premi Ctrl+C.

## Dati

La modalità predefinita prova a scaricare i dati della stagione NBA corrente dalla libreria pubblica `nba_api`, senza chiavi API e senza costi. Per evitare di presentare dati vecchi come aggiornati, l'app mostra un errore se il servizio non è raggiungibile, invece di passare silenziosamente ai dati dimostrativi. L'aggiornamento dipende dalla disponibilità e dai limiti del servizio NBA Stats: potrebbe non funzionare in ogni rete o momento.

È disponibile anche una modalità CSV. Le colonne richieste sono indicate nell'interfaccia.

## Limiti

Le stime usano statistiche recenti e un modello semplice, non dati sugli infortuni o formazioni confermate e non un modello validato. Le probabilità non sono garanzie e l'app non piazza scommesse.
