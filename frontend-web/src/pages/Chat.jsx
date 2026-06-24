import { useState } from 'react'

export default function Chat() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([
    { role: 'assistant', content: 'Como foi o treino de hoje? Alguma dor articular ou fadiga excessiva?' }
  ])

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = { role: 'user', content: message }
    const newHistory = [...history, userMessage]
    setHistory(newHistory)
    setMessage('')
    setLoading(true)

    try {
      // Chama o endpoint FastAPI local
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          history: history.slice(1) // Envia o histórico (sem a saudação inicial local se quiser, ou com ela)
        })
      });
      const data = await res.json();
      
      setHistory(prev => [...prev, { role: 'assistant', content: data.reply_message }])
      
      console.log("Métricas Extraídas silenciosamente:", data.extracted_data)
      
    } catch (err) {
      console.error(err);
      setHistory(prev => [...prev, { role: 'assistant', content: 'Desculpe, ocorreu um erro na conexão com o cérebro.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-content">
      <header>
        <h1 className="title">ATENDENTE IA</h1>
        <p className="subtitle">Relate dores ou atualize seu peso</p>
      </header>

      <div className="chat-container">
        {history.map((msg, index) => (
          <div key={index} className={`chat-bubble ${msg.role === 'assistant' ? 'bot' : 'user-bubble'}`}>
            {msg.content}
          </div>
        ))}
        {loading && <div className="chat-bubble bot">Pensando...</div>}
      </div>

      <div className="action-container chat-input-area">
        <textarea 
          className="text-input" 
          placeholder="Ex: Hoje eu acordei pesando 81kg..."
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        <button className="main-button small-btn" onClick={handleSend} disabled={loading}>
          {loading ? 'ENVIANDO...' : 'ENVIAR RELATO'}
        </button>
      </div>
    </div>
  )
}

