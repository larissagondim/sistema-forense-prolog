const CHARACTERS = [
  {
    id: "larissa",
    nome: "Larissa",
    avatar: "👩‍💻",
    local: "Sala Principal",
    naCena: true,
    habilidade: "Desativar laser",
    habilidadeRelevante: true,
    alibi: null,
    descricao:
      "Especialista em segurança eletrônica. Foi vista na sala principal na noite do roubo. Não apresentou álibi.",
  },
  {
    id: "maria",
    nome: "Maria",
    avatar: "👩‍🎨",
    local: "Sala Principal",
    naCena: true,
    habilidade: "Manipular objetos",
    habilidadeRelevante: true,
    alibi: null,
    descricao:
      "Restauradora de obras de arte com acesso à sala principal. Habilidade em manusear objetos pesados. Sem álibi confirmado.",
  },
  {
    id: "laura",
    nome: "Laura",
    avatar: "👷‍♀️",
    local: "Corredor",
    naCena: false,
    habilidade: "Limpeza",
    habilidadeRelevante: false,
    alibi: "Confirmado",
    descricao:
      "Funcionária de limpeza do museu. Estava no corredor, fora da sala principal. Possui álibi confirmado por câmeras.",
  },
];

function Badge({ children, variant = "neutral" }) {
  const styles = {
    danger: "bg-red-500/15 text-red-400 border-red-500/20",
    success: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/15 text-amber-400 border-amber-500/20",
    neutral: "bg-neutral-500/15 text-neutral-400 border-neutral-500/20",
  };

  return (
    <span
      className={`text-xs font-medium px-2.5 py-1 rounded-full border ${styles[variant]}`}
    >
      {children}
    </span>
  );
}

function InfoRow({ label, value, badge }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-neutral-800 last:border-0">
      <span className="text-neutral-500 text-sm">{label}</span>
      {badge || <span className="text-neutral-200 text-sm font-medium">{value}</span>}
    </div>
  );
}

export default function CharacterCards({ onSelect }) {
  return (
    <section className="min-h-screen px-4 py-16">
      <div className="max-w-5xl mx-auto animate-fade-in-up">
        <p className="text-gold-400 tracking-[0.3em] uppercase text-sm font-medium mb-4 text-center">
          Dossiê dos Suspeitos
        </p>
        <h2 className="font-serif text-4xl md:text-5xl font-bold text-gold-100 mb-4 text-center">
          Quem é a culpada?
        </h2>
        <p className="text-neutral-400 text-center mb-12 max-w-xl mx-auto">
          Analise o perfil de cada suspeita e selecione quem você acredita ser a
          responsável pelo roubo.
        </p>

        <div className="grid md:grid-cols-3 gap-6">
          {CHARACTERS.map((char, i) => (
            <button
              key={char.id}
              onClick={() => onSelect(char.id)}
              className="group bg-surface-light border border-neutral-800 rounded-2xl p-6 text-left transition-all duration-300 hover:border-gold-500/50 hover:shadow-[0_0_40px_rgba(184,134,11,0.1)] hover:scale-[1.02] cursor-pointer"
              style={{ animationDelay: `${i * 150}ms` }}
            >
              <div className="text-5xl mb-4">{char.avatar}</div>

              <h3 className="font-serif text-2xl font-bold text-gold-200 mb-2 group-hover:text-gold-300 transition-colors">
                {char.nome}
              </h3>

              <p className="text-neutral-400 text-sm mb-5 leading-relaxed">
                {char.descricao}
              </p>

              <div className="space-y-0">
                <InfoRow label="Local" value={char.local} />
                <InfoRow
                  label="Na cena?"
                  badge={
                    char.naCena ? (
                      <Badge variant="danger">Sim</Badge>
                    ) : (
                      <Badge variant="success">Não</Badge>
                    )
                  }
                />
                <InfoRow
                  label="Habilidade"
                  badge={
                    <Badge
                      variant={char.habilidadeRelevante ? "warning" : "neutral"}
                    >
                      {char.habilidade}
                    </Badge>
                  }
                />
                <InfoRow
                  label="Álibi"
                  badge={
                    char.alibi ? (
                      <Badge variant="success">{char.alibi}</Badge>
                    ) : (
                      <Badge variant="danger">Sem álibi</Badge>
                    )
                  }
                />
              </div>

              <div className="mt-6 py-3 rounded-xl bg-gold-500/10 text-gold-400 text-center font-semibold text-sm border border-gold-500/20 group-hover:bg-gold-500/20 transition-colors">
                Selecionar como culpada
              </div>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
