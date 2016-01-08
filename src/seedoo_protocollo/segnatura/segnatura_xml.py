# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
import dateutil
from lxml import etree
from datetime import datetime
# from seedoo_protocollo.model.protocollo import protocollo_protocollo


class SegnaturaXML:

    def __init__(self, protocollo, prot_number, prot_date, cr, uid):
        self.protocollo = protocollo
        self.prot_number = prot_number
        date_object = dateutil.parser.parse(prot_date)
        self.prot_date = date_object
        self.prot_type = protocollo.type
        self.cr = cr
        self.uid = uid

        self.pooler = protocollo.pool
        self.resUsersObj = self.pooler.get("res.users")
        self.protocolloObj = self.pooler.get("protocollo.protocollo")
        self.resCompanyObj = self.pooler.get("res.company")
        self.irAttachmentObj = self.pooler.get("ir.attachment")

        self.currentUser = self.resUsersObj.browse(cr, uid, uid)
        companyId = self.currentUser.company_id.id
        self.company = self.resCompanyObj.browse(cr, uid, companyId)

        if self.company.ident_code != False:
            self.codiceAOO = str(self.company.ident_code)
        else:
            self.codiceAOO = None

        print "ciao"
        pass

    def generate_segnatura_root(self):
        root = etree.Element("Segnatura")
        intestazione = self.create_intestazione()
        descrizione = self.createDescrizione()
        root.append(intestazione)
        root.append(descrizione)
        return root

    def createDescrizione(self):
        descrizione = etree.Element("Descrizione")

        attachments = self.irAttachmentObj.search(self.cr, self.uid, [('res_model','=', 'protocollo.protocollo'), ('res_id','=',6)])

        docObj = self.protocollo.doc_id
        if docObj:
            documento = self.createDocumento(docObj)
            descrizione.append(documento)
            # attachments.remove(docObj.id)

        if len(attachments) > 1:
            allegati = self.createAllegati(attachments)
            descrizione.append(allegati)

        # testoDelMessaggio = etree.Element("TestoDelMessaggio")
        # descrizione.append(testoDelMessaggio)

        # note = etree.Element("Note")
        # descrizione.append(note)
        return descrizione

    def createDocumento(self, document):
        documento = etree.Element("Documento", nome=document.name, tiporiferimento="MIME")

        return documento

    def createAllegati(self, attachments):
        allegati = etree.Element("Allegati")
        for attachment in attachments:
                attachmentObj = self.irAttachmentObj.browse(self.cr, self.uid, attachment)
                if attachmentObj is not None:
                    documento = self.createDocumento(attachmentObj)
                    allegati.append(documento)
        # fascicolo = self.createFascicolo()
        # allegati.append(fascicolo)
        return allegati

    def createFascicolo(self):
        fascicolo = etree.Element("Fascicolo")
        codiceAmministrazione = self.createCodiceAmministrazione()
        codiceAOO = self.createCodiceAOO()
        oggetto = self.createOggetto()
        identificativo = etree.Element("Identificativo")
        classifica = self.createClassifica()
        note = etree.Element("Note")
        documento = self.createDocumento(None)
        # fascicolo = etree.Element("Fascicolo")

        fascicolo.append(codiceAmministrazione)
        fascicolo.append(codiceAOO)
        fascicolo.append(oggetto)
        fascicolo.append(identificativo)
        fascicolo.append(classifica)
        fascicolo.append(note)
        fascicolo.append(documento)
        return fascicolo

    def createClassifica(self):
        classifica = etree.Element("Classifica")
        codiceAmministrazione = self.createCodiceAmministrazione()
        codiceAOO = self.createCodiceAOO()
        denominazione = etree.Element("Denominazione")
        livello = etree.Element("Livello")

        classifica.append(codiceAmministrazione)
        classifica.append(codiceAOO)
        classifica.append(denominazione)
        classifica.append(livello)

        return classifica

    def create_intestazione(self):
        intestazione = etree.Element("Intestazione")
        identificatore = self.createIdentificatore()
        intestazione.append(identificatore)

        if self.prot_type == "in":
            origine = self.createOrigineIN()
            intestazione.append(origine)

            destinazione = self.createDestinazioneIN()
            intestazione.append(destinazione)

            # observers = self.protocollo.assigne_cc
            # for observer in observers:
            #     perConoscenza = self.createPerConoscenza(observer)
            #     intestazione.append(perConoscenza)

        oggetto = self.createOggetto()
        intestazione.append(oggetto)
        return intestazione

    def createOggetto(self):
        oggetto = etree.Element("Oggetto")
        oggetto.text = self.checkNullValue(self.protocollo.subject)

        return oggetto

    def createOggettoFascicolo(self):
        oggetto = etree.Element("Oggetto")
        return oggetto

    def createDestinazioneIN(self):
        destinazione = etree.Element("Destinazione")
        indirizzoTelematico = self.createIndirizzoTelematicoFromCompany(self.company)
        destinatario = self.createDestinatarioIN()

        destinazione.append(indirizzoTelematico)
        destinazione.append(destinatario)
        return destinazione

    def createPerConoscenza(self):
        destinazione = etree.Element("Destinazione")
        # indirizzoTelematico = self.createIndirizzoTelematico()
        # destinatario = self.createDestinatario()

        # destinazione.append(indirizzoTelematico)
        # destinazione.append(destinatario)
        return destinazione

    def createDestinatarioIN(self):
        destinatario = etree.Element("Destinatario")
        amministrazione = self.createAmministrazioneIN(self.company)
        destinatario.append(amministrazione)

        return destinatario

    def createDestinatario(self):
        destinatario = etree.Element("Destinatario")
        amministrazione = self.createAmministrazione()
        aOO = self.createAOO()
        privato = self.createPrivatoFromSenderReceiver()

        destinatario.append(amministrazione)
        destinatario.append(aOO)
        destinatario.append(privato)
        return destinatario



    def createIdentificatore(self):
        identificatore = etree.Element("Identificatore")
        # TODO Recuperare da qualche parte il codice amministrazione (codice IPA??)
        codiceAmministrazione = self.createCodiceAmministrazione()
        codiceAOO = self.createCodiceAOO(self.codiceAOO)
        numeroRegistrazione = self.createNumeroRegistrazione(self.prot_number)
        dataRegistrazione = self.createDataRegistrazione(self.prot_date)
        identificatore.append(codiceAmministrazione)
        identificatore.append(codiceAOO)
        identificatore.append(numeroRegistrazione)
        identificatore.append(dataRegistrazione)
        return identificatore

    def createDataRegistrazione(self, dataRegistrazioneVal):
        dataRegistrazione = etree.Element("DataRegistrazione")
        dataRegistrazione.text = dataRegistrazioneVal.date().isoformat()
        return dataRegistrazione

    def createNumeroRegistrazione(self, numeroRegistrazioneVal):
        numeroRegistrazione = etree.Element("NumeroRegistrazione")
        numeroRegistrazione.text = numeroRegistrazioneVal
        return numeroRegistrazione

    def createCodiceAOO(self, codiceAOOVal = ""):
        codiceAOO = etree.Element("CodiceAOO")
        codiceAOO.text = codiceAOOVal
        return codiceAOO

    def createCodiceAmministrazione(self):
        # TODO Recuperare da qualche parte il codice amministrazione (codice IPA??)
        codiceAmministrazione = etree.Element("CodiceAmministrazione")
        return codiceAmministrazione

    def createOrigine(self, senderReceiver):
        origine = etree.Element("Origine")
        indirizzoTelematico = self.createIndirizzoTelematicoFromSenderReceiver(senderReceiver)
        mittente = self.createMittente(senderReceiver)
        origine.append(indirizzoTelematico)
        origine.append(mittente)
        return origine

    def createOrigineIN(self):
        origine = etree.Element("Origine")
        # indirizzoTelematico = self.createIndirizzoTelematicoFromSenderReceiver(senderReceiver)
        # origine.append(indirizzoTelematico)
        senders = self.protocollo.sender_receivers
        for sender in senders:
            mittente = self.createMittente(sender)
            origine.append(mittente)
        return origine

    def createIndirizzoTelematicoFromSenderReceiver(self, senderReceiver):
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        indirizzoTelematicoVal = ""
        if senderReceiver.pec_mail:
            indirizzoTelematicoVal = senderReceiver.pec_mail
        elif senderReceiver.email:
            indirizzoTelematicoVal = senderReceiver.email

        indirizzoTelematico.text = indirizzoTelematicoVal
        return indirizzoTelematico

    def createIndirizzoTelematicoFromCompany(self, company):
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        indirizzoTelematicoVal = ""
        if company.email:
            indirizzoTelematicoVal = company.email

        indirizzoTelematico.text = indirizzoTelematicoVal
        return indirizzoTelematico

    def createMittente(self, senderReceiver):
        mittente = etree.Element("Mittente")

        # TODO creare una discriminante per le pubbliche amministrazioni
        # amministrazione = self.createAmministrazione(senderReceiver)
        # aOO = self.createAOO()
        # mittente.append(amministrazione)
        # mittente.append(aOO)

        privato = self.createPrivatoFromSenderReceiver(senderReceiver)
        mittente.append(privato)

        return mittente

    def createPrivatoFromSenderReceiver(self, senderReceiver):
        privato = etree.Element("Privato")
        if senderReceiver.type == "legal":
            privato.attrib["tipo"] = "impresa"
            denominazioneImpresa = self.createDenominazioneImpresa(senderReceiver)
            privato.append(denominazioneImpresa)
            partitaIva = etree.Element("PartitaIva")
            privato.append(partitaIva)
        elif senderReceiver.type == "individual":
            privato.attrib["tipo"] = "cittadino"
            nome = self.createNome(senderReceiver)
            privato.append(nome)
            cognome = etree.Element("Cognome")
            # privato.append(cognome)
            codiceFiscale = etree.Element("CodiceFiscale")
            # privato.append(codiceFiscale)

        identificativo = self.createIdentificativo()
        indirizzoTelematico = self.createIndirizzoTelematicoFromSenderReceiver(senderReceiver)
        indirizzoPostale = self.createIndirizzoPostaleFromSenderReceiver(senderReceiver)
        telefono = self.createTelefono(senderReceiver)

        privato.append(identificativo)
        privato.append(indirizzoTelematico)
        privato.append(indirizzoPostale)
        privato.append(telefono)
        return privato

    def createPrivatoFromCompany(self, company):
        privato = etree.Element("Privato")
        if company.type == "legal":
            privato.attrib["tipo"] = "impresa"
            denominazioneImpresa = self.createDenominazioneImpresa(company)
            privato.append(denominazioneImpresa)
            partitaIva = etree.Element("PartitaIva")
            privato.append(partitaIva)
        elif company.type == "individual":
            privato.attrib["tipo"] = "cittadino"
            nome = self.createNome(company)
            privato.append(nome)
            cognome = etree.Element("Cognome")
            # privato.append(cognome)
            codiceFiscale = etree.Element("CodiceFiscale")
            # privato.append(codiceFiscale)

        identificativo = self.createIdentificativo()
        indirizzoTelematico = self.createIndirizzoTelematicoFromSenderReceiver(company)
        indirizzoPostale = self.createIndirizzoPostale(company)
        telefono = self.createTelefono(company)

        privato.append(identificativo)
        privato.append(indirizzoTelematico)
        privato.append(indirizzoPostale)
        privato.append(telefono)
        return privato

    def createTelefono(self, senderReceiver):
        telefono = etree.Element("Telefono")
        telefonoValue = ""
        if hasattr(senderReceiver, "mobile") and senderReceiver.mobile:
            telefonoValue = senderReceiver.mobile
        elif senderReceiver.phone:
            telefonoValue = senderReceiver.phone

        telefono.text = self.checkNullValue(telefonoValue)
        return telefono

    def createNome(self, senderReceiver):
        nome = etree.Element("Nome")
        nome.text = self.checkNullValue(senderReceiver.name)
        return nome

    def createDenominazioneImpresa(self, senderReceiver):
        denominazioneImpresa = etree.Element("DenominazioneImpresa")
        denominazioneImpresa.text = self.checkNullValue(senderReceiver.name)
        return denominazioneImpresa

    def createIdentificativo(self):
        return etree.Element("Identificativo")

    def createAOO(self):
        aOO = etree.Element("AOO")
        denominazione = self.createDenominazione()
        codiceAOO = self.createCodiceAOO()

        aOO.append(denominazione)
        aOO.append(codiceAOO)
        return aOO

    def createAOOFromDepartment(self, department):
        aOO = etree.Element("AOO")
        denominazione = self.createDenominazione()
        denominazioneVal = ""
        if hasattr(department, "name") and department.name:
            denominazioneVal = department.name
        denominazione.text = denominazioneVal
        codiceAOO = self.createCodiceAOO()

        aOO.append(denominazione)
        aOO.append(codiceAOO)
        return aOO

    def createDenominazione(self, denominazioneVal=""):
        denominazione = etree.Element("Denominazione")
        denominazione.text = denominazioneVal
        return denominazione

    def createAmministrazione(self, senderReceiver):
        amministrazione = etree.Element("Amministrazione")
        denominazione = self.createDenominazione(senderReceiver.name)
        # TODO Recuperare da qualche parte il codice amministrazione (codice IPA??)
        codiceAmministrazione = self.createCodiceAmministrazione()
        unitaOrganizzativa = self.createUnitaOrganizzativaFromSenderReceiver(senderReceiver)

        amministrazione.append(denominazione)
        amministrazione.append(codiceAmministrazione)
        amministrazione.append(unitaOrganizzativa)
        return amministrazione

    def createAmministrazioneIN(self, company):
        amministrazione = etree.Element("Amministrazione")
        denominazione = self.createDenominazione(company.name)
        amministrazione.append(denominazione)

        # TODO Recuperare da qualche parte il codice amministrazione (codice IPA??)
        codiceAmministrazione = self.createCodiceAmministrazione()
        amministrazione.append(codiceAmministrazione)

        assignees = self.protocollo.assigne
        for assignee in assignees:
            unitaOrganizzativa = self.createUnitaOrganizzativaFromDepartment(assignee)
            amministrazione.append(unitaOrganizzativa)

        return amministrazione

    def createUnitaOrganizzativaFromSenderReceiver(self, senderReceiver):
        unitaOrganizzativa = etree.Element("UnitaOrganizzativa", tipo="permanente")
        denominazione = self.createDenominazione(senderReceiver.name)
        # identificativo = self.createIdentificativo()
        indirizzoPostale = self.createIndirizzoPostaleFromSenderReceiver(senderReceiver)
        indirizzoTelematico = self.createIndirizzoTelematicoFromSenderReceiver(senderReceiver)
        telefono = self.createTelefono(senderReceiver)
        fax = etree.Element("Fax")

        unitaOrganizzativa.append(denominazione)
        # unitaOrganizzativa.append(identificativo)
        unitaOrganizzativa.append(indirizzoPostale)
        unitaOrganizzativa.append(indirizzoTelematico)
        unitaOrganizzativa.append(telefono)
        unitaOrganizzativa.append(fax)
        return unitaOrganizzativa

    def createUnitaOrganizzativaFromDepartment(self, department):
        company = self.company
        unitaOrganizzativa = etree.Element("UnitaOrganizzativa", tipo="permanente")
        denominazione = self.createDenominazione(department.name)
        # identificativo = self.createIdentificativo()
        indirizzoPostale = self.createIndirizzoPostaleFromCompany(company)
        indirizzoTelematico = self.createIndirizzoTelematicoFromCompany(company)
        telefono = self.createTelefono(company)
        fax = etree.Element("Fax")

        unitaOrganizzativa.append(denominazione)
        # unitaOrganizzativa.append(identificativo)
        unitaOrganizzativa.append(indirizzoPostale)
        unitaOrganizzativa.append(indirizzoTelematico)
        unitaOrganizzativa.append(telefono)
        unitaOrganizzativa.append(fax)
        return unitaOrganizzativa

    def createIndirizzoPostaleFromSenderReceiver(self, senderReceiver):
        indirizzoPostale = etree.Element("IndirizzoPostale")
        toponimo = etree.Element("Toponimo")
        toponimo.text = self.checkNullValue(senderReceiver.street)
        # TODO estrarre il civico dall'indirizzo
        civico = etree.Element("Civico")
        cap = self.createCap(senderReceiver.zip)
        comune = self.createComune(senderReceiver.city)

        # TODO recuperare la provincia da qualche parte o modellarla o fottersene
        provincia = etree.Element("Provincia")
        nazione = self.createNazione(senderReceiver.country_id)

        indirizzoPostale.append(toponimo)
        indirizzoPostale.append(civico)
        indirizzoPostale.append(cap)
        indirizzoPostale.append(comune)
        indirizzoPostale.append(provincia)
        indirizzoPostale.append(nazione)
        return indirizzoPostale

    def createIndirizzoPostaleFromCompany(self, company):
        indirizzoPostale = etree.Element("IndirizzoPostale")
        toponimo = etree.Element("Toponimo")
        toponimo.text = self.checkNullValue(company.street)
        # TODO estrarre il civico dall'indirizzo
        civico = etree.Element("Civico")
        cap = self.createCap(company.zip)
        comune = self.createComune(company.city)

        # TODO recuperare la provincia da qualche parte o modellarla o fottersene
        provincia = etree.Element("Provincia")
        nazione = self.createNazione(company.country_id)

        indirizzoPostale.append(toponimo)
        indirizzoPostale.append(civico)
        indirizzoPostale.append(cap)
        indirizzoPostale.append(comune)
        indirizzoPostale.append(provincia)
        indirizzoPostale.append(nazione)
        return indirizzoPostale

    def createComune(self, comuneVal):
        comune = etree.Element("Comune")
        comuneValue = ""
        if comuneVal:
            comuneValue = comuneVal
        comune.text = comuneValue
        return comune

    def createNazione(self, nazioneObj):
        nazione = etree.Element("Nazione")
        nazioneValue = ""
        if nazioneObj and nazioneObj.name:
            nazioneValue = nazioneObj.name
        nazione.text = nazioneValue
        return nazione

    def createCap(self, capVal):
        cap = etree.Element("CAP")
        cap.text = self.checkNullValue(capVal)
        return cap

    def checkNullValue(self, value):
        tempValue = ""
        if value:
            tempValue = value
        return tempValue
