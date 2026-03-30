import { useState } from "react";
import StorySection from "./components/StorySection";
import CharacterCards from "./components/CharacterCard";
import ResultReveal from "./components/ResultReveal";

const STEPS = { STORY: 0, CHARACTERS: 1, RESULT: 2 };

export default function App() {
  const [step, setStep] = useState(STEPS.STORY);
  const [selectedId, setSelectedId] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function handleSelect(id) {
    setSelectedId(id);
    setStep(STEPS.RESULT);
  }

  async function handleRestart() {
    await fetch("/api/nova-rodada", { method: "POST" });
    setSelectedId(null);
    setRefreshKey((k) => k + 1);
    setStep(STEPS.CHARACTERS);
  }

  function handleBackToStart() {
    setSelectedId(null);
    setStep(STEPS.STORY);
  }

  if (step === STEPS.STORY) {
    return <StorySection onStart={() => setStep(STEPS.CHARACTERS)} />;
  }

  if (step === STEPS.CHARACTERS) {
    return <CharacterCards key={refreshKey} onSelect={handleSelect} />;
  }

  return (
    <ResultReveal
      selectedId={selectedId}
      onRestart={handleRestart}
      onBackToStart={handleBackToStart}
    />
  );
}
