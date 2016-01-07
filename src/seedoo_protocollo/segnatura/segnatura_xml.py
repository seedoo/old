# -*- coding: utf-8 -*-
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from lxml import etree
# from seedoo_protocollo.model.protocollo import protocollo_protocollo


class SegnaturaXML:

    def __init__(self, protocollo, cr, uid):
        self.protocollo = protocollo
        pooler = protocollo.pool
        resUsersObj = pooler.get("res.users")
        protocolloObj = pooler.get("protocollo.protocollo")
        resCompanyObj = pooler.get("res.company")

        self.currentUser = resUsersObj.browse(cr, uid, uid)
        companyId = self.currentUser.company_id.id
        self.company = resCompanyObj.browse(cr, uid, companyId)

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
        documento = etree.Element("Documento")
        testoDelMessaggio = etree.Element("TestoDelMessaggio")
        allegati = self.createAllegati()
        note = etree.Element("Note")

        descrizione.append(documento)
        # descrizione.append(testoDelMessaggio)
        descrizione.append(allegati)
        descrizione.append(note)
        return descrizione

    def createAllegati(self):
        allegati = etree.Element("Allegati")
        documento = etree.Element("Documento")
        fascicolo = self.createFascicolo()

        allegati.append(documento)
        allegati.append(fascicolo)
        return allegati

    def createFascicolo(self):
        fascicolo = etree.Element("Fascicolo")
        codiceAmministrazione = self.createCodiceAmministrazione()
        codiceAOO = etree.Element("CodiceAOO")
        oggetto = etree.Element("Oggetto")
        identificativo = etree.Element("Identificativo")
        classifica = self.createClassifica()
        note = etree.Element("Note")
        documento = etree.Element("Documento")
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
        codiceAOO = etree.Element("CodiceAOO")
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
        origine = self.createOrigine()
        destinazione = self.createDestinazione()
        perConoscenza = self.createDestinazione()
        oggetto = etree.Element("Oggetto")
        intestazione.append(identificatore)
        intestazione.append(origine)
        intestazione.append(destinazione)
        intestazione.append(perConoscenza)
        intestazione.append(oggetto)
        return intestazione


    def createDestinazione(self):
        destinazione = etree.Element("Destinazione")
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        destinatario = self.createDestinatario()

        destinazione.append(indirizzoTelematico)
        destinazione.append(destinatario)
        return destinazione

    def createDestinatario(self):
        destinatario = etree.Element("Destinatario")
        amministrazione = self.createAmministrazione()
        aOO = self.createAOO()
        privato = self.createPrivato()

        destinatario.append(amministrazione)
        destinatario.append(aOO)
        destinatario.append(privato)
        return destinatario

    def createIdentificatore(self):
        identificatore = etree.Element("Identificatore")
        codiceAmministrazione = self.createCodiceAmministrazione()
        codiceAOO = etree.Element("CodiceAOO")
        numeroRegistrazione = etree.Element("NumeroRegistrazione")
        dataRegistrazione = etree.Element("DataRegistrazione")
        identificatore.append(codiceAmministrazione)
        identificatore.append(codiceAOO)
        identificatore.append(numeroRegistrazione)
        identificatore.append(dataRegistrazione)
        return identificatore

    def createCodiceAmministrazione(self):
        codiceAmministrazione = etree.Element("CodiceAmministrazione")
        return codiceAmministrazione

    def createOrigine(self):
        origine = etree.Element("Origine")
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        mittente = self.createMittente()
        origine.append(indirizzoTelematico)
        origine.append(mittente)
        return origine

    def createMittente(self):
        mittente = etree.Element("Mittente")
        amministrazione = self.createAmministrazione()
        aOO = self.createAOO()
        privato = self.createPrivato()

        mittente.append(amministrazione)
        mittente.append(aOO)
        mittente.append(privato)

        return mittente

    def createPrivato(self):
        privato = etree.Element("Privato")
        identificativo = self.createIdentificativo()
        denominazioneImpresa = etree.Element("DenominazioneImpresa")
        partitaIva = etree.Element("PartitaIva")
        nome = etree.Element("Nome")
        cognome = etree.Element("Cognome")
        codiceFiscale = etree.Element("CodiceFiscale")
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        indirizzoPostale = self.createIndirizzoPostale()
        telefono = etree.Element("Telefono")

        privato.append(identificativo)
        privato.append(denominazioneImpresa)
        privato.append(partitaIva)
        privato.append(nome)
        privato.append(cognome)
        privato.append(codiceFiscale)
        privato.append(indirizzoTelematico)
        privato.append(indirizzoPostale)
        privato.append(telefono)
        return privato

    def createIdentificativo(self):
        return etree.Element("Identificativo")

    def createAOO(self):
        aOO = etree.Element("AOO")
        denominazione = self.createDenominazione()
        codiceAOO = etree.Element("CodiceAOO")

        aOO.append(denominazione)
        aOO.append(codiceAOO)
        return aOO

    def createDenominazione(self):
        denominazione = etree.Element("Denominazione")
        return denominazione

    def createAmministrazione(self):
        amministrazione = etree.Element("Amministrazione")
        denominazione = self.createDenominazione()
        codiceAmministrazione = self.createCodiceAmministrazione()
        unitaOrganizzativa = self.createUnitaOrganizzativa()

        amministrazione.append(denominazione)
        amministrazione.append(codiceAmministrazione)
        amministrazione.append(unitaOrganizzativa)
        return amministrazione

    def createUnitaOrganizzativa(self):
        unitaOrganizzativa = etree.Element("UnitaOrganizzativa", tipo="permanente")
        denominazione = self.createDenominazione()
        identificativo = self.createIdentificativo()
        indirizzoPostale = self.createIndirizzoPostale()
        indirizzoTelematico = etree.Element("IndirizzoTelematico")
        telefono = etree.Element("Telefono")
        fax = etree.Element("Fax")

        unitaOrganizzativa.append(denominazione)
        unitaOrganizzativa.append(identificativo)
        unitaOrganizzativa.append(indirizzoPostale)
        unitaOrganizzativa.append(indirizzoTelematico)
        unitaOrganizzativa.append(telefono)
        unitaOrganizzativa.append(fax)
        return unitaOrganizzativa

    def createIndirizzoPostale(self):
        indirizzoPostale = etree.Element("IndirizzoPostale")
        toponimo = etree.Element("Toponimo")
        civico = etree.Element("Civico")
        cap = etree.Element("CAP")
        comune = etree.Element("Comune")
        provincia = etree.Element("Provincia")
        nazione = etree.Element("Nazione")

        indirizzoPostale.append(toponimo)
        indirizzoPostale.append(civico)
        indirizzoPostale.append(cap)
        indirizzoPostale.append(comune)
        indirizzoPostale.append(provincia)
        indirizzoPostale.append(nazione)
        return indirizzoPostale
