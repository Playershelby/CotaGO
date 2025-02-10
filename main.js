   // main.js
   import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.3.0/firebase-auth .js";

   // Função para verificar o estado de autenticação
   const checkAuthState = (callback) => {
       onAuthStateChanged(auth, (user) => {
           if (user) {
               console.log("Usuário autenticado:", user);
               callback(user);
           } else {
               console.log("Nenhum usuário autenticado.");
               callback(null);
           }
       });
   };

   // Adicionando o evento de clique ao botão de login
   document.getElementById("login-button").addEventListener("click", async () => {
       const email = document.getElementById("email-input").value;
       const password = document.getElementById("password-input").value;
       try {
           await loginUser (email, password);
           window.location.href = "/templates/home.html"; // Redirecionar após o login
       } catch (error) {
           alert("Erro ao fazer login. Verifique suas credenciais.");
       }
   });