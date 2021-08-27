// var fs = require("fs");
// var text = fs.readFileSync("file://Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt");
// var textByLine = text.split("\n")
// document.write(text);

// var txtFile = new XMLHttpRequest();
// txtFile.open("GET", "file://Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt", true);
// txtFile.onreadystatechange = function() {
//   if (txtFile.readyState === 4) {  // Makes sure the document is ready to parse.
//     if (txtFile.status === 200) {  // Makes sure it's found the file.
//       allText = txtFile.responseText;
//       lines = txtFile.responseText.split("\n"); // Will separate each line into an array
//     }
//   }
// }
// txtFile.send(null);
// document.write(txtFile.responseText)

// var fileName = "file://Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt";
//
// var txtFile;
// if (window.XMLHttpRequest)
// {// code for IE7+, Firefox, Chrome, Opera, Safari
// txtFile = new XMLHttpRequest();
// }
// else
// {// code for IE6, IE5
// txtFile = new ActiveXObject("Microsoft.XMLHTTP");
// }
// txtFile.open("GET",fileName,false);
// txtFile.send();
// var txtDoc=txtFile.responseText;
// var lines = txtDoc.split("\r\n"); // values in lines[0], lines[1]...
//
// document.write(txtFile.responseText)

 ("#text").load("file://Users/Michael/Documents/Work/UNSW/Work/QC_reports/text_files/Deployment.txt");
