function verifynotify(field1, field2) {
 this.field1 = field1;
 this.field2 = field2;

 this.check = function() {

   if (this.field1.value != "" && this.field1.value != this.field2.value) {
      alert("Passwords do not match!");
   }
 }
}