#!/bin/sh
# This file is part of Seedoo.  The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

BD=$(dirname $0)
CP=$BD/lib/itextpdf-5.5.3.jar
CP=$CP:$BD/lib/itext-xtra-5.5.3.jar
CP=$CP:$BD/lib/itext-pdfa-5.5.3.jar
CP=$CP:$BD/lib/bcprov-jdk15on-151.jar
CP=$CP:$BD/lib/bcprov-ext-jdk15on-151.jar
CP=$CP:$BD/lib/Signature.jar
echo $BD
echo $CP
#cd $BD/bin/com/innoviu/signature
java -cp "$CP" com.innoviu.signature.Signature $1 "$2" $3
