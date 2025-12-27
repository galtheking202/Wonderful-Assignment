db = db.getSiblingDB("mydb");

db.users.insertMany([
  { id: 1, name_en: "Alice", name_he: "אליס", age: 30, prescription_medicens: [1, 2],credits:100 },
  { id: 2, name_en: "Bob", name_he: "בוב", age: 40, prescription_medicens: [],credits:100 },
  { id: 3, name_en: "Charlie", name_he: "צ'רלי", age: 25, prescription_medicens: [],credits:100 },
  { id: 4, name_en: "David", name_he: "דוד", age: 35, prescription_medicens: [],credits:100 },
  { id: 5, name_en: "Eve", name_he: "חווה", age: 28, prescription_medicens: [1],credits:100 },
  { id: 6, name_en: "Frank", name_he: "פרנק", age: 50, prescription_medicens: [],credits:100 },
  { id: 7, name_en: "Grace", name_he: "גרייס", age: 22, prescription_medicens: [],credits:100 },
  { id: 8, name_en: "Hannah", name_he: "חנה", age: 31, prescription_medicens: [2],credits:100 },
  { id: 9, name_en: "Ivy", name_he: "איווי", age: 27, prescription_medicens: [],credits:100 },
  { id: 10, name_en: "Jack", name_he: "ג'ק", age: 45, prescription_medicens: [1],credits:100 }
]);

db.medicens_stock.insertMany([
  { id: 1, medicine_name_en: "Amoxicillin",medicine_name_he:"אמוקסיצילין" ,prescription:true,inventory:100,credit_cost:10},
  { id: 2, medicine_name_en: "Atorvastatin",medicine_name_he:"אטורווסטאטין" ,prescription:true,inventory:50,credit_cost:15},
  { id: 3, medicine_name_en: "Advil",medicine_name_he:"אדוויל" ,prescription:false,inventory:200,credit_cost:5},
  { id: 4, medicine_name_en: "Zyrtec",medicine_name_he:"זירטק" ,prescription:false,inventory:150,credit_cost:8},
  { id: 5, medicine_name_en: "Akamol",medicine_name_he:"אקמול" ,prescription:false,inventory:75,credit_cost:12},
  { id: 6, medicine_name_en: "Tylenol",medicine_name_he:"טילנול" ,prescription:false,inventory:120,credit_cost:7}
]);
