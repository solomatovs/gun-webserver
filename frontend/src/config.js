// Можно в будущем вынести в process.env.*
// (vite поддерживает переменные окружения через import.meta.env)

const config = {
    gatewayUrl: "https://gate.muduck.com",   // адрес Gateway API
    defaultUserId: "user123"                // пока статично
  };
  
  export default config;