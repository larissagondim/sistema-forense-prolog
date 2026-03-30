import { useEffect, useState } from "react";

const NAMES = { larissa: "Larissa", maria: "Maria Luíza", laura: "Laura" };

const PROF_AVATARS = {
  restauradora: "👩‍🎨",
  curadora: "👩‍💼",
  historiadora: "👩‍🏫",
};

const LOCAL_LABELS = {
  sala_principal: "Sala Principal",
  sala_seguranca: "Sala de Segurança",
  corredor: "Corredor",
};

const DIGITAL_LABELS = {
  mensagens_apagadas: "Mensagens apagadas",
  historico_apagado: "Histórico apagado",
  fotos_recentes: "Fotos recentes",
};

const PROF_LABELS = {
  restauradora: "Restauradora",
  curadora: "Curadora",
  historiadora: "Historiadora",
};

const PROF_DESC = {
  restauradora: "Restauradora de obras de arte. Endividada, reclamação constante do salário.",
  curadora: "Curadora de acervo. Acha que a obra não deveria estar no museu.",
  historiadora: "Historiadora especialista em arte. Briga recente com superior.",
};

function Badge({ children, variant = "neutral" }) {
  const styles = {
    danger: "bg-red-500/15 text-red-400 border-red-500/20",
    success: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/15 text-amber-400 border-amber-500/20",
    neutral: "bg-neutral-500/15 text-neutral-400 border-neutral-500/20",
  };

  return (
    <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${styles[variant]}`}>
      {children}
    </span>
  );
}

function InfoRow({ label, badge }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-neutral-800 last:border-0">
      <span className="text-neutral-500 text-sm">{label}</span>
      {badge}
    </div>
  );
}

function weightVariant(points, max) {
  if (points >= max) return "danger";
  if (points >= max / 2) return "warning";
  return "neutral";
}

export default function CharacterCards({ onSelect }) {
  const [suspeitos, setSuspeitos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/suspeitos")
      .then((r) => r.json())
      .then((data) => setSuspeitos(data.sort(() => Math.random() - 0.5)))
      .catch((err) => console.error("Erro:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <section className="min-h-screen flex items-center justify-center">
        <div className="text-gold-400 text-xl animate-pulse font-serif">
          Carregando dossiês...
        </div>
      </section>
    );
  }

  return (
    <section className="min-h-screen px-4 py-16">
      <div className="max-w-5xl mx-auto animate-fade-in-up">
        <p className="text-gold-400 tracking-[0.3em] uppercase text-sm font-medium mb-2 text-center">
          Dossiê dos Suspeitos
        </p>
        <h2 className="font-serif text-4xl md:text-5xl font-bold text-gold-100 mb-4 text-center">
          Quem é a culpada?
        </h2>
        <p className="text-neutral-400 text-center mb-12 max-w-xl mx-auto">
          Analise as evidências de cada suspeita e selecione quem você acredita
          ser a responsável pelo roubo.
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {suspeitos.map((s, i) => {
            const d = s.detalhes;
            return (
              <button
                key={s.nome}
                onClick={() => onSelect(s.nome)}
                className="group bg-surface-light border border-neutral-800 rounded-2xl p-6 text-left transition-all duration-300 hover:border-gold-500/50 hover:shadow-[0_0_40px_rgba(46,125,50,0.1)] hover:scale-[1.02] cursor-pointer"
                style={{ animationDelay: `${i * 150}ms` }}
              >
                <div className="text-5xl mb-4">{PROF_AVATARS[d.profissao] || "👤"}</div>

                <h3 className="font-serif text-2xl font-bold text-gold-200 mb-4 group-hover:text-gold-300 transition-colors">
                  {NAMES[s.nome] || s.nome}
                </h3>

                <div className="space-y-0">
                  <InfoRow
                    label="Localização"
                    badge={<Badge>{LOCAL_LABELS[d.local] || d.local}</Badge>}
                  />
                  <InfoRow
                    label="Rastro digital"
                    badge={<Badge>{DIGITAL_LABELS[d.digital] || d.digital}</Badge>}
                  />
                  <div className="py-2 border-b border-neutral-800">
                    <div className="flex justify-between items-center">
                      <span className="text-neutral-500 text-sm">Profissão</span>
                      <Badge>{PROF_LABELS[d.profissao] || d.profissao}</Badge>
                    </div>
                    <p className="text-neutral-500 text-xs italic mt-1.5 leading-relaxed">
                      {PROF_DESC[d.profissao]}
                    </p>
                  </div>
                  <InfoRow
                    label="Álibi"
                    badge={
                      <Badge>{d.alibi === "nao" ? "Sem álibi" : "Com álibi"}</Badge>
                    }
                  />
                </div>

                <div className="mt-6 py-3 rounded-xl bg-gold-500/10 text-gold-400 text-center font-semibold text-sm border border-gold-500/20 group-hover:bg-gold-500/20 transition-colors">
                  Selecionar como culpada
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
