import { login } from "./api/api";

const loginForm = document.getElementById("login-form") as HTMLFormElement;
const message = document.getElementById("message")!;



loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = (document.getElementById("username") as HTMLInputElement).value;
  const password = (document.getElementById("password") as HTMLInputElement).value;

  const token = await login(username, password);

  if (token) {
    localStorage.setItem("token", token);
    window.location.href = "/reserva.html";
  } else {
    message.textContent = "Credenciales inválidas ❌";
  }
});
