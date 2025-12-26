db = db.getSiblingDB("mydb");

db.users.insertMany([
  { id: 1, name: "Alice", age: 30 },
  { id: 2, name: "Bob", age: 40 },
  { id: 3, name: "Charlie", age: 25 },
  { id: 4, name: "David", age: 35 },
  { id: 5, name: "Eve", age: 28 },
  { id: 6, name: "Frank", age: 50 },
  { id: 7, name: "Grace", age: 22 },
  { id: 8, name: "Hannah", age: 31 },
  { id: 9, name: "Ivy", age: 27 },
  { id: 10, name: "Jack", age: 45 }
]);

db.medicens_stock.insertMany([
  { id: 1, medicine_id: 1, medicine_name: "Amoxicillin" ,prescription:true},
  { id: 2, medicine_id: 2, medicine_name: "Atorvastatin" ,prescription:true},
  { id: 3, medicine_id: 3, medicine_name: "Advil" ,prescription:false},
  { id: 4, medicine_id: 4, medicine_name: "Zyrtec" ,prescription:false},
  { id: 5, medicine_id: 5, medicine_name: {"en":"Tylenol","he":"טילנול"} ,prescription:false}
]);
