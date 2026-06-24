import React, { useState } from 'react';
import { UploadCloud, CheckCircle2 } from 'lucide-react';

export default function Physique() {
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      // Simulando o envio para o Gemini 2.5 Flash Vision
      setAnalyzing(true);
      setTimeout(() => {
        setResult({
          weak_points: ["Posterior de ombro", "Panturrilhas"],
          asymmetries: ["Braço esquerdo levemente menor"],
          emphasis_suggestion: "Focar em exercícios de isolamento para panturrilhas (2x na semana) e adicionar elevação lateral curvada para o deltoide posterior.",
          recommended_exercise_adjustments: ["+ Elevação Lateral Curvada", "+ Gêmeos Sentado"]
        });
        setAnalyzing(false);
      }, 3000);
    }
  };

  return (
    <div className="page-content">
      <header>
        <h1 className="title">ANÁLISE FÍSICA</h1>
        <p className="subtitle">Envie uma foto e a Inteligência Artificial avaliará seus pontos fracos e assimetrias.</p>
      </header>

      <div className="card" style={{ textAlign: 'center', padding: '48px 24px' }}>
        {!file && !analyzing && !result && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <UploadCloud size={64} color="#FF5722" />
            <h2 style={{ fontFamily: 'Bebas Neue', fontSize: '32px' }}>UPLOAD DA FOTO ATUAL</h2>
            <p className="subtitle">Formatos aceitos: JPG, PNG (Max 5MB)</p>
            <label className="main-button" style={{ display: 'inline-flex', alignItems: 'center', cursor: 'pointer', marginTop: '16px' }}>
              Selecionar Foto
              <input type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileChange} />
            </label>
          </div>
        )}

        {analyzing && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <div className="spinner" style={{ border: '4px solid #333', borderTop: '4px solid #FF5722', borderRadius: '50%', width: '48px', height: '48px', animation: 'spin 1s linear infinite' }}></div>
            <h2 style={{ fontFamily: 'Bebas Neue', fontSize: '32px' }}>O GEMINI ESTÁ ANALISANDO SEU FÍSICO...</h2>
            <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
          </div>
        )}

        {result && !analyzing && (
          <div style={{ textAlign: 'left' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
              <CheckCircle2 color="#4CAF50" size={32} />
              <h2 style={{ fontFamily: 'Bebas Neue', fontSize: '32px', color: '#4CAF50' }}>ANÁLISE CONCLUÍDA</h2>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <strong style={{ color: '#FF5722' }}>Pontos Fracos Detectados:</strong>
                <ul style={{ paddingLeft: '20px', marginTop: '8px', color: '#A0A0A0' }}>
                  {result.weak_points.map((p, i) => <li key={i}>{p}</li>)}
                </ul>
              </div>

              <div>
                <strong style={{ color: '#FF5722' }}>Assimetrias:</strong>
                <ul style={{ paddingLeft: '20px', marginTop: '8px', color: '#A0A0A0' }}>
                  {result.asymmetries.map((p, i) => <li key={i}>{p}</li>)}
                </ul>
              </div>

              <div>
                <strong style={{ color: '#FF5722' }}>Sugestão de Treino:</strong>
                <p style={{ marginTop: '8px', color: '#A0A0A0', lineHeight: '1.5' }}>{result.emphasis_suggestion}</p>
              </div>

              <div style={{ marginTop: '16px' }}>
                <button className="main-button" onClick={() => {setFile(null); setResult(null);}}>Nova Análise</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
