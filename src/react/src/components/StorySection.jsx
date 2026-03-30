export default function StorySection({ onStart }) {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 py-8">
      <div className="max-w-2xl w-full animate-fade-in-up text-center">
        <p className="text-gold-400 tracking-[0.3em] uppercase text-xs font-medium mb-4">
          Caso #0042 — Confidencial
        </p>

        <h1 className="font-serif text-4xl md:text-5xl font-bold text-gold-100 mb-6 leading-tight">
          O Roubo no <span className="text-gold-400">Grande Museu</span>
        </h1>

        <div className="bg-surface-light border border-gold-600/20 rounded-xl p-6 md:p-8 text-left space-y-4 text-neutral-300 leading-relaxed text-[15px]">
          <p>
            Na noite passada, uma obra de valor inestimável desapareceu da{" "}
            <strong className="text-gold-300">Sala Principal</strong> do Grande
            Museu.
          </p>
          <p>
            A polícia confirmou a presença de{" "}
            <strong className="text-gold-300">12 pessoas</strong> no Grande
            Museu no momento do roubo: 3 na Sala Principal, 2 na Sala de
            Segurança e 7 nos Corredores.
          </p>
          <p>
            Um deles foi preso em flagrante com notas de dinheiro vivo:{" "}
            <strong className="text-gold-300">Luis Augusto</strong>, segurança
            do museu. Com medo da prisão, fez um acordo para diminuir a pena ao
            delatar que tinha um total de{" "}
            <strong className="text-gold-300">6 pessoas envolvidas</strong> no
            crime: 2 na Sala Principal, 1 na Sala de Segurança e 3 nos
            Corredores, sendo ele um dos 3 envolvidos nos Corredores.
          </p>
          <p>
            Temendo a própria vida, decidiu não entregar nenhum culpado porém,
            querendo diminuir ainda mais a pena, falou{" "}
            <strong className="text-gold-300">3 funcionárias do museu</strong>{" "}
            garantindo que uma delas está envolvida.
          </p>
          <p className="text-gold-200 font-semibold text-base mt-1">
            Sua função, Detetive, é analisar as evidências e descobrir qual
            delas é culpada: Larissa, Laura ou Maria Luíza.
          </p>
        </div>

        <button
          onClick={onStart}
          className="mt-8 px-9 py-3.5 bg-gold-500 hover:bg-gold-400 text-surface font-bold rounded-xl text-base tracking-wide transition-all duration-300 cursor-pointer hover:scale-105 hover:shadow-[0_0_30px_rgba(46,125,50,0.3)]"
        >
          Iniciar Investigação
        </button>
      </div>
    </section>
  );
}
