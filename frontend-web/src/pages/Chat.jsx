import { useState } from 'react'

export default function Chat() {
  const [message, setMessage] = useState('')

  return (
    <div className="page-content">
      <header>
        <h1 className="title">AJUSTE IA</h1>
        <p className="subtitle">Relate dores ou fadiga para ajustar regras</p>
      </header>

      <div className="chat-container">
        <div className="chat-bubble bot">
          Como foi o treino de hoje? Alguma dor articular ou fadiga excessiva?
        </div>
      </div>

      <div className="action-container chat-input-area">
        <textarea 
          className="text-input" 
          placeholder="Ex: Senti dor no ombro esquerdo..."
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        <button className="main-button small-btn">
          ENVIAR RELATO
        </button>
      </div>
    </div>
  )
}
