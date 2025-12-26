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

db.medicens_stoc.insertMany([
  { id: 1, medicen_id: 1, diagnosis: "Asthma" },
  { id: 2, user_id: 2, diagnosis: "Diabetes" },
  { id: 3, user_id: 3, diagnosis: "Hypertension" },
  { id: 4, user_id: 4, diagnosis: "Allergy" },
  { id: 5, user_id: 5, diagnosis: "Flu" }
]);
