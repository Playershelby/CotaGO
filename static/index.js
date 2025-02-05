// Adicione as bibliotecas do Firebase ao seu app
<script src="https://www.gstatic.com/firebasejs/11.2.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/11.2.0/firebase-firestore-compat.js"></script>

// Inicialize o Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();


function login() {
    // Lógica de login aqui
    alert("Login clicado!"); // Exemplo de ação
}

db.collection("usuarios").add({
    nome: "João",
    sobrenome: "Marcos",
    data: "04202001",
    CPF: "00011100035",
    email: "marcos.db@gmail.com",
    senha: "Marcos@23"
})
.then((docRef) => {
    console.log("Documento escrito com ID: ", docRef.id);
})
.catch((error) => {
    console.error("Erro ao adicionar documento: ", error);
});

db.collection("usuarios").get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data()}`);
    });
});