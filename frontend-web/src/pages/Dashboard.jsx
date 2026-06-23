export default function Dashboard() {
  return (
    <div className="page-content">
      <header>
        <h1 className="title">VISÃO GERAL</h1>
        <p className="subtitle">Resumo diário</p>
      </header>

      <div className="card-list">
        <div className="card">
          <span className="card-title">PESO ATUAL</span>
          <span className="card-value">80.5 <span className="unit">KG</span></span>
        </div>
        
        <div className="card">
          <span className="card-title">MACROS (CUTTING)</span>
          <div className="macros-row">
            <div className="macro"><span className="m-val">176</span><span className="m-lbl">PRO</span></div>
            <div className="macro"><span className="m-val">130</span><span className="m-lbl">CARB</span></div>
            <div className="macro"><span className="m-val">80</span><span className="m-lbl">FAT</span></div>
          </div>
          <span className="card-value highlight-text mt-2">1948 <span className="unit">KCAL</span></span>
        </div>
      </div>
    </div>
  )
}
