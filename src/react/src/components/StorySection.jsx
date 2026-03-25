export default function StorySection({ onStart }) {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 py-16">
      <div className="max-w-3xl w-full animate-fade-in-up text-center">
        <p className="text-gold-400 tracking-[0.3em] uppercase text-sm font-medium mb-6">
          Caso #0042 — Confidencial
        </p>

        <h1 className="font-serif text-5xl md:text-6xl font-bold text-gold-100 mb-8 leading-tight">
          O Roubo no
          <br />
          <span className="text-gold-400">Grande Museu</span>
        </h1>

        <div className="bg-surface-light border border-gold-600/20 rounded-2xl p-8 md:p-10 text-left space-y-5 text-neutral-300 leading-relaxed text-lg">
          <p>
            Na noite passada, uma obra de valor inestimável desapareceu da{" "}
            <strong className="text-gold-300">sala principal</strong> do Grande
            Museu. O sistema de segurança registrou a ativação de dois sensores
            críticos:{" "}
            <strong className="text-gold-300">laser e pressão de peso</strong>,
            confirmando que houve atividade no local.
          </p>
          <p>
            Para realizar o crime, o responsável precisaria de habilidades
            específicas:{" "}
            <strong className="text-gold-300">desativar o sistema laser</strong>{" "}
            e{" "}
            <strong className="text-gold-300">
              manipular objetos pesados
            </strong>{" "}
            sem acionar alarmes adicionais.
          </p>
          <p>
            Três pessoas foram identificadas nas proximidades do museu naquela
            noite. Cada uma possui perfil, habilidades e álibis distintos.
          </p>
          <p className="text-gold-200 font-semibold">
            Analise as evidências e decida: quem você acredita ser a culpada?
          </p>
        </div>

        <button
          onClick={onStart}
          className="mt-10 px-10 py-4 bg-gold-500 hover:bg-gold-400 text-surface font-bold rounded-xl text-lg tracking-wide transition-all duration-300 cursor-pointer hover:scale-105 hover:shadow-[0_0_30px_rgba(184,134,11,0.3)]"
        >
          Iniciar Investigação
        </button>
      </div>
    </section>
  );
}
