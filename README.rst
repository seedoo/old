.. image:: http://www.seedoo.it/wp-content/uploads/2015/05/Seedoo%E2%80%93logo-02.svg
   :alt: Seedoo
   :target: http://www.seedoo.it

La piattaforma software di nuova generazione per la digitalizzazione della PA.

Il software gestisce l’intero iter documentale in maniera personalizzata e integrata, seguendo i procedimenti interni del tuo Ente, dalla generazione e acquisizione del documento alla pubblicazione online secondo le norme sulla trasparenza.

Protocollo informatico, Gestione Documentale, Analisi dei Dati, sono alcuni degli strumenti che permettono alla nuova PA di perseguire i propri obiettivi in un’ottica di performance, governance e trasparenza verso il cittadino

.. image:: https://travis-ci.org/seedoo/seedoo.svg?branch=master
    :target: https://travis-ci.org/seedoo/seedoo/branches

Installazione
=============
La seguente procedura è stata testata su Ubuntu Server e dovrebbe funzionare su ogni distribuzione Debian based

Prerequisiti
------------
PostgreSQL
^^^^^^^^^^
`http://www.postgresql.org/download/ <http://www.postgresql.org/download/>`_

Git
^^^
`https://git-scm.com/downloads <https://git-scm.com/downloads>`_

Segnatura
^^^^^^^^^
Java

``OpenJDK 64-Bit Server VM: java version 1.7``

Buildout
^^^^^^^^
`Installing build dependencies <http://pythonhosted.org/anybox.recipe.odoo/first_steps.html#installing-build-dependencies>`_

Configurazione ambiente
-----------------------
Buildout
^^^^^^^^
Eseguire i seguenti comandi nel path dove si vuole installare seedoo e con l’utente di sistema che dovrà eseguirlo

``git clone https://github.com/seedoo/seedoo.git``

``cd seedoo``

``wget https://raw.github.com/buildout/buildout/master/bootstrap/bootstrap.py``

``virtualenv sandbox``

``sandbox/bin/pip install unidecode==0.04.17``

``sandbox/bin/pip install python-magic==0.4.6``

``sandbox/bin/pip install PyXB==1.2.4``

``sandbox/bin/pip install pyPdf==1.13``

``sandbox/bin/pip uninstall setuptools pip``

``sandbox/bin/python bootstrap.py``

Segnatura
^^^^^^^^^
Sempre nel path di seedoo, eseguire

``mkdir /opt/signature``

``cp -r extras/lib /opt/signature``

``cp extras/signature.sh /opt/signature``

``chmod u+x /opt/signature/signature.sh``

Opzioni personali
-----------------
Configurare le proprie impostazioni nel file ``buildout.cfg``

``options.admin_passwd``

``options.db_host``

``options.db_password``

``options.db_user``

La ``admin_passwd`` verrà usata per creare ed eliminare i database.

Le opzioni ``db_host``, ``db_password`` e ``db_user`` dipendono dalla propria configurazione di PostgreSQL. Ad esempio, se si usa postgresql in locale ed è stato creato l'utente ``seedoo`` con password ``seedoo``, le opzioni saranno

``options.db_host = localhost``

``options.db_password = seedoo``

``options.db_user = seedoo``

Buildout
--------
Per creare l'istanza, eseguire quindi

``bin/buildout``

Avvio istanza
-------------
Eseguire

``bin/start_odoo``

A questo punto è possibile accedere al sistema all’URL

``http://localhost:8069``

Configurazione segnatura
------------------------
Fare il login a seedoo con l’utente admin e cliccare

``Configuration -> Technical -> Parameters -> Technical Parameters``

Creare un nuovo record con i seguenti valori

``Key = itext.location``

``Value = '/opt/signature'``
