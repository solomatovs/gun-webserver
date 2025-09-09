import React, { useState } from "react";
import { useWorkerWS } from "./hooks/useWorkerWS.js";

function App() {
  const [userId, setUserId] = useState("user123");
  const { messages, status, send } = useWorkerWS(userId);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Realtime Worker Output</h1>
      <p>Status: {status}</p>

      <div>
        <input
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="User ID"
        />
      </div>

      <button onClick={() => send("hello from frontend")}>
        Send Message
      </button>

      <ul>
        {messages.map((msg, idx) => (
          <li key={idx}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;