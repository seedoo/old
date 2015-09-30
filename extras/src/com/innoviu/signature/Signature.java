/* This file is part of Seedoo.  The COPYRIGHT file at the top level of
this module contains the full copyright notices and license terms. */

package com.innoviu.signature;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import com.itextpdf.text.BaseColor;
import com.itextpdf.text.DocumentException;
import com.itextpdf.text.pdf.BaseFont;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.PdfStamper;
import com.itextpdf.text.pdf.PdfContentByte;

public class Signature {
	
	  private static void maintain(String path) {
		  try {
			  File maintain = new File(path + ".enc");
			  maintain.createNewFile();
		} catch (IOException e) {
			e.printStackTrace();
		}
	  }	
	
	  private static void fail(String path) {
		  try {
			  File fail = new File(path + ".fail");
			  fail.createNewFile();
		} catch (IOException e) {
			e.printStackTrace();
		}
	  }
	
	  public static void main(String[] args) {
		boolean isEncrypted = false;
		boolean isFailed = false;
		try {
			if (args.length < 2) {
				throw new FileNotFoundException();
			}
			  PdfReader reader = new PdfReader(args[0]);
			  isEncrypted = reader.isEncrypted();
			  String suffix = ".pdf";
			  if (isEncrypted) {
				  System.out.println("Encrypted");
				  String[] cmd = {"pdftk",  args[0], "output", args[0] + ".pdftk.pdf"};
				    try{
				        Process proc = Runtime.getRuntime().exec( cmd );
				        proc.waitFor();
				    }
				    catch(Exception e){
				        System.out.println("Exception is:"+e);
				    }
				    reader = new PdfReader(args[0] + ".pdftk.pdf");
				    suffix = ".dec.pdf";
			  }
			  PdfStamper stamper = new PdfStamper(reader, new FileOutputStream(args[0] + suffix));
			  PdfContentByte over = stamper.getOverContent(1);
			  String type = args[2];
			  int xpos = 0;
			  //int xpos = (type == "in") ? 120 : 10;
			  if ("in".equals(type)) {
				  xpos = 0;
			  } else {
				  xpos = 120;
			  }
			  over.setColorFill(BaseColor.WHITE);
			  over.rectangle(xpos + 10, 8, 120, 8);
			  over.fill();
			  over.beginText();
			  BaseFont bf_times = BaseFont.createFont(BaseFont.TIMES_ROMAN, "Cp1252", false);
			  over.setFontAndSize(bf_times, 6);
			  over.setColorFill(BaseColor.BLACK);
			  over.showTextAligned(PdfContentByte.ALIGN_RIGHT, args[1], 120 + xpos, 10, 0);
			  over.endText();
			  stamper.close();
			  if (isEncrypted) {
				  File file = new File(args[0] + ".pdftk.pdf");
				  file.delete();
			  }
		} catch (FileNotFoundException e) {
			isFailed = true;
			e.printStackTrace();
		} catch (DocumentException e) {
			isFailed = true;
			e.printStackTrace();
		} catch (IOException e) {
			isFailed = true;
			e.printStackTrace();
		} finally {
			if (isEncrypted) {
				maintain(args[0]);
			} else if (isFailed){
				fail(args[0]);
			} else {
				
			}
		}
	}

}
