import { useEffect, useRef, useState } from "react";
import { createSession } from "../api.js";
import config from "../config.js";

export function useWorkerWS(userId = config.defaultUserId) {
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("disconnected");
  const wsRef = useRef(null);

  useEffect(() => {
    let intervalId;

    async function init() {
      try {
        setStatus("connecting");

        // 1. создаём сессию через Gateway
        const session = await createSession(userId);

        // 2. подключаемся к WebSocket воркера
        const ws = new WebSocket(
          `wss://${session.host}:${session.port}/ws?token=${session.token}&user_id=${session.user_id}`
        );
        wsRef.current = ws;

        ws.onopen = () => {
          setStatus("connected");
          console.log("✅ Connected to worker");
        };

        ws.onmessage = (event) => {
          setMessages((prev) => [...prev, event.data]);
        };

        ws.onclose = () => {
          setStatus("disconnected");
          console.log("❌ Disconnected");
        };

        // 3. пинги
        intervalId = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send("ping");
          }
        }, 5000);

      } catch (err) {
        console.error("Session init error:", err);
        setStatus("error");
      }
    }

    init();

    return () => {
      clearInterval(intervalId);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [userId]);

  function send(msg) {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(msg);
    }
  }

  return { messages, status, send };
}