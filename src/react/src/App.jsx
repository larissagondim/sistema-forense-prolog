import { useState } from "react";
import StorySection from "./components/StorySection";
import CharacterCards from "./components/CharacterCard";
import ResultReveal from "./components/ResultReveal";

const STEPS = { STORY: 0, CHARACTERS: 1, RESULT: 2 };

export default function App() {
  const [step, setStep] = useState(STEPS.STORY);
  const [selectedId, setSelectedId] = useState(null);

  function handleSelect(id) {
    setSelectedId(id);
    setStep(STEPS.RESULT);
  }

  function handleRestart() {
    setSelectedId(null);
    setStep(STEPS.STORY);
  }

  if (step === STEPS.STORY) {
    return <StorySection onStart={() => setStep(STEPS.CHARACTERS)} />;
  }

  if (step === STEPS.CHARACTERS) {
    return <CharacterCards onSelect={handleSelect} />;
  }

  return <ResultReveal selectedId={selectedId} onRestart={handleRestart} />;
}
