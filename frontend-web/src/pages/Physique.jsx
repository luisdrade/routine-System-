export default function Physique() {
  return (
    <div className="page-content">
      <header>
        <h1 className="title">ANÁLISE FÍSICA</h1>
        <p className="subtitle">Avaliação via Claude Sonnet</p>
      </header>

      <div className="action-container">
        <div className="card text-center mb-4">
          <p className="subtitle">Faça upload de uma foto do seu físico atual para receber análise de assimetrias e sugestões de ênfase.</p>
        </div>
        <button className="main-button small-btn">
          ENVIAR FOTO
        </button>
      </div>
    </div>
  )
}
