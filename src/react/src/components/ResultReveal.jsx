import { useEffect, useState } from "react";

const NAMES = { larissa: "Larissa", maria: "Maria Luíza", laura: "Laura" };

const PROF_AVATARS = {
  restauradora: "👩‍🎨",
  curadora: "👩‍💼",
  historiadora: "👩‍🏫",
};

function SuspectResult({ s, isSelected, isGuilty }) {
  return (
    <div
      className={`bg-surface-light border rounded-2xl p-6 transition-all ${
        isSelected
          ? "border-gold-500/60 shadow-[0_0_30px_rgba(46,125,50,0.15)]"
          : "border-neutral-800"
      }`}
    >
      <div className="flex items-center gap-4">
        <span className="text-4xl">
          {PROF_AVATARS[s.detalhes?.profissao] || "👤"}
        </span>
        <div className="flex-1">
          <h3 className="font-serif text-xl font-bold text-gold-200">
            {NAMES[s.nome] || s.nome}
          </h3>
          <p className={`text-sm font-semibold mt-1 ${isGuilty ? "text-red-400" : "text-emerald-400"}`}>
            {isGuilty ? "Culpada" : "Inocente"} — {s.pontuacao} pontos
          </p>
        </div>
        {isSelected && (
          <span className="text-xs font-medium px-3 py-1 rounded-full bg-gold-500/15 text-gold-400 border border-gold-500/20">
            Sua escolha
          </span>
        )}
      </div>
    </div>
  );
}

export default function ResultReveal({ selectedId, onRestart, onBackToStart }) {
  const [suspeitos, setSuspeitos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/suspeitos")
      .then((r) => r.json())
      .then((data) => setSuspeitos(data))
      .catch((err) => console.error("Erro:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <section className="min-h-screen flex items-center justify-center">
        <div className="text-gold-400 text-xl animate-pulse font-serif">
          Analisando evidências...
        </div>
      </section>
    );
  }

  const topSuspect = suspeitos[0]?.nome;
  const guessedCorrectly = selectedId === topSuspect;

  return (
    <section className="min-h-screen px-4 py-16">
      <div className="max-w-2xl mx-auto animate-fade-in-up">
        <p className="text-gold-400 tracking-[0.3em] uppercase text-sm font-medium mb-2 text-center">
          Resultado da Investigação
        </p>

        <h2 className="font-serif text-4xl md:text-5xl font-bold text-center mb-3">
          {guessedCorrectly ? (
            <span className="text-emerald-400">Excelente, Detetive!</span>
          ) : (
            <span className="text-red-400">Quase lá, Detetive...</span>
          )}
        </h2>

        <p className="text-neutral-400 text-center mb-10 text-lg">
          {guessedCorrectly
            ? `Você acertou! ${NAMES[topSuspect]} era a culpada.`
            : `A culpada era ${NAMES[topSuspect]}, não ${NAMES[selectedId]}.`}
        </p>

        <div className="space-y-4">
          {suspeitos.map((s) => (
            <SuspectResult
              key={s.nome}
              s={s}
              isSelected={s.nome === selectedId}
              isGuilty={s.nome === topSuspect}
            />
          ))}
        </div>

        <div className="flex gap-4 justify-center mt-10">
          <button
            onClick={onRestart}
            className="px-8 py-3 bg-gold-500 hover:bg-gold-400 text-surface font-bold rounded-xl transition-all duration-300 cursor-pointer hover:scale-105"
          >
            Nova Rodada
          </button>
          <button
            onClick={onBackToStart}
            className="px-8 py-3 border border-gold-500/30 hover:border-gold-500/60 text-gold-400 font-bold rounded-xl transition-all duration-300 cursor-pointer hover:scale-105"
          >
            Voltar ao Início
          </button>
        </div>
      </div>
    </section>
  );
}
