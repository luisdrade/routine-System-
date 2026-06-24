import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const weightData = [
  { date: '01/06', weight: 87.5 },
  { date: '08/06', weight: 86.8 },
  { date: '15/06', weight: 86.0 },
  { date: '22/06', weight: 85.0 },
  { date: '29/06', weight: 84.2 },
];

export default function Dashboard() {
  return (
    <div className="page-content">
      <header>
        <h1 className="title">VISÃO GERAL</h1>
        <p className="subtitle">Acompanhe seu progresso e metas diárias.</p>
      </header>

      <div className="card-list">
        {/* Card de Peso Atual */}
        <div className="card">
          <div className="card-title">PESO ATUAL</div>
          <div>
            <span className="card-value">84.2</span>
            <span className="unit"> kg</span>
          </div>
          <p className="subtitle" style={{ fontSize: '14px', marginTop: '8px' }}>
            <span className="highlight-text">-3.3 kg</span> desde o mês passado
          </p>
        </div>

        {/* Card de Nutrição (Macros) */}
        <div className="card">
          <div className="card-title">META DE NUTRIÇÃO (CUTTING)</div>
          <div className="macros-row">
            <div className="macro">
              <span className="m-val">2100</span>
              <span className="m-lbl">KCAL</span>
            </div>
            <div className="macro">
              <span className="m-val">180<span style={{fontSize: '16px'}}>g</span></span>
              <span className="m-lbl">PROT</span>
            </div>
            <div className="macro">
              <span className="m-val">200<span style={{fontSize: '16px'}}>g</span></span>
              <span className="m-lbl">CARB</span>
            </div>
            <div className="macro">
              <span className="m-val">65<span style={{fontSize: '16px'}}>g</span></span>
              <span className="m-lbl">GORD</span>
            </div>
          </div>
        </div>
      </div>

      {/* Gráfico de Evolução de Peso */}
      <div className="card" style={{ marginTop: '16px' }}>
        <div className="card-title">EVOLUÇÃO DE PESO</div>
        <div style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={weightData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="date" stroke="#A0A0A0" tick={{ fill: '#A0A0A0' }} axisLine={false} tickLine={false} />
              <YAxis domain={['dataMin - 1', 'dataMax + 1']} stroke="#A0A0A0" tick={{ fill: '#A0A0A0' }} axisLine={false} tickLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                itemStyle={{ color: '#FF5722', fontWeight: 'bold' }}
              />
              <Line 
                type="monotone" 
                dataKey="weight" 
                stroke="#FF5722" 
                strokeWidth={3}
                dot={{ fill: '#FF5722', r: 4 }}
                activeDot={{ r: 6, fill: '#FFFFFF', stroke: '#FF5722', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
