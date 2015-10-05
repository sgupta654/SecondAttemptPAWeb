function verifynotify(field1, field2, result_id, match_html, nomatch_html) {
 this.field1 = field1;
 this.field2 = field2;
 this.result_id = result_id;
 this.match_html = match_html;
 this.nomatch_html = nomatch_html;

 this.check = function() {

   // Make sure we don't cause an error
   // for browsers that do not support getElementById
   if (!this.result_id) { return false; }
   if (!document.getElementById){ return false; }
   r = document.getElementById(this.result_id);
   if (!r){ return false; }

   if (this.field1.value != "" && this.field1.value == this.field2.value) {
     r.innerHTML = this.match_html;
   } else {
     r.innerHTML = this.nomatch_html;
   }
 }
}