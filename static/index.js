
// Inicialize o Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();


// Função para verificar o estado de autenticação
firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
        // Usuário está autenticado
        console.log("Usuário autenticado:", user);
    } else {
        // Nenhum usuário está autenticado
        console.log("Nenhum usuário autenticado.");
    }
});

// Função para verificar se o token de ID é válido
async function checkIdToken() {
    const user = firebase.auth().currentUser ;
    if (user) {
        try {
            const idToken = await user.getIdToken(true);
            console.log("Token de ID válido:", idToken);
            // Você pode enviar o token para o seu backend para validação
        } catch (error) {
            console.error("Erro ao obter o token de ID:", error);
        }
    } else {
        console.log("Nenhum usuário autenticado para verificar o token.");
    }
}

// Função para autenticar o usuário
async function loginUser (email, password) {
    try {
        const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
        // Usuário autenticado
        const user = userCredential.user;
        console.log("Login feito com sucesso !", user);
        // Redirecionar ou realizar outras ações após o login
    } catch (error) {
        console.error("Falha no Login...", error.message);
        // Exibir mensagem de erro para o usuário
    }
}

// Adicionando o evento de clique ao botão de login
document.getElementById("login-button").addEventListener("click", function() {
    const email = document.getElementById("email-input").value;
    const password = document.getElementById("password-input").value;
    loginUser (email, password);
});

// Verificar o estado de autenticação
firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
        // Se o usuário já estiver autenticado, redirecionar para home.html
        window.location.href = "home.html";
    }
});

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


//Ler DB Usuario
db.collection("usuarios").get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data()}`);
    });
});