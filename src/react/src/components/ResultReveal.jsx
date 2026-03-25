import { useEffect, useState } from "react";

const NAMES = { larissa: "Larissa", maria: "Maria", laura: "Laura" };

function ScoreBar({ label, points }) {
  const filled = points > 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-neutral-400 text-sm w-44 shrink-0">{label}</span>
      <div className="flex-1 h-3 bg-neutral-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${filled ? "bg-gold-400" : "bg-neutral-700"}`}
          style={{ width: filled ? "100%" : "0%" }}
        />
      </div>
      <span className="text-gold-300 font-bold text-sm w-6 text-right">
        +{points}
      </span>
    </div>
  );
}

function SuspectResult({ data, isUserPick }) {
  const nivelStyles = {
    alta: { bg: "bg-red-500/15", border: "border-red-500/30", text: "text-red-400", label: "ALTA" },
    media: { bg: "bg-amber-500/15", border: "border-amber-500/30", text: "text-amber-400", label: "MÉDIA" },
    baixa: { bg: "bg-emerald-500/15", border: "border-emerald-500/30", text: "text-emerald-400", label: "BAIXA" },
  };

  const style = nivelStyles[data.nivel] || nivelStyles.baixa;
  const lines = data.texto.split("\n").filter((l) => l.startsWith("- "));

  const scoreMap = lines.map((line) => {
    const match = line.match(/\(\+(\d)\)/);
    return { label: line.replace(/\s*\(\+\d\)/, "").replace("- ", ""), points: match ? parseInt(match[1]) : 0 };
  });

  return (
    <div
      className={`${style.bg} ${style.border} border rounded-2xl p-6 md:p-8 ${isUserPick ? "ring-2 ring-gold-400/50" : ""}`}
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="font-serif text-2xl font-bold text-gold-100">
            {NAMES[data.nome] || data.nome}
          </h3>
          {isUserPick && (
            <span className="text-gold-400 text-xs tracking-widest uppercase">
              Seu palpite
            </span>
          )}
        </div>
        <div className="text-right">
          <div className={`text-3xl font-bold ${style.text}`}>
            {data.pontuacao}/4
          </div>
          <span className={`text-xs font-semibold ${style.text}`}>
            {style.label} suspeita
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {scoreMap.map((s, i) => (
          <ScoreBar key={i} label={s.label} points={s.points} />
        ))}
      </div>
    </div>
  );
}

export default function ResultReveal({ selectedId, onRestart }) {
  const [suspeitos, setSuspeitos] = useState([]);
  const [explicacoes, setExplicacoes] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [suspRes, ...expRes] = await Promise.all([
          fetch("/api/suspeitos").then((r) => r.json()),
          ...["larissa", "maria", "laura"].map((n) =>
            fetch(`/api/explicacao/${n}`).then((r) => r.json())
          ),
        ]);

        setSuspeitos(suspRes);

        const expMap = {};
        expRes.forEach((e) => {
          expMap[e.nome] = e.texto;
        });
        setExplicacoes(expMap);
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
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

  const culpados = suspeitos.filter((s) => s.nivel === "alta");
  const acertou = culpados.some((c) => c.nome === selectedId);

  const merged = suspeitos.map((s) => ({
    ...s,
    texto: explicacoes[s.nome] || "",
  }));

  const selectedFirst = [...merged].sort((a, b) => {
    if (a.nome === selectedId) return -1;
    if (b.nome === selectedId) return 1;
    return b.pontuacao - a.pontuacao;
  });

  return (
    <section className="min-h-screen px-4 py-16">
      <div className="max-w-3xl mx-auto animate-fade-in-up">
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">{acertou ? "✅" : "❌"}</div>
          <h2 className="font-serif text-4xl md:text-5xl font-bold mb-4">
            {acertou ? (
              <span className="text-emerald-400">Palpite correto!</span>
            ) : (
              <span className="text-red-400">Palpite incorreto</span>
            )}
          </h2>
          <p className="text-neutral-400 text-lg max-w-xl mx-auto">
            {acertou
              ? `${NAMES[selectedId]} é de fato uma das culpadas identificadas pelo sistema Prolog.`
              : `${NAMES[selectedId]} não é culpada segundo a análise. Veja abaixo o resultado completo.`}
          </p>
        </div>

        <p className="text-gold-400 tracking-[0.3em] uppercase text-sm font-medium mb-6 text-center">
          Análise completa do sistema Prolog
        </p>

        <div className="space-y-6">
          {selectedFirst.map((data) => (
            <SuspectResult
              key={data.nome}
              data={data}
              isUserPick={data.nome === selectedId}
            />
          ))}
        </div>

        <div className="text-center mt-12">
          <button
            onClick={onRestart}
            className="px-10 py-4 bg-surface-lighter border border-gold-600/30 hover:border-gold-400/50 text-gold-300 font-semibold rounded-xl text-lg transition-all duration-300 cursor-pointer hover:scale-105"
          >
            Investigar novamente
          </button>
        </div>
      </div>
    </section>
  );
}
