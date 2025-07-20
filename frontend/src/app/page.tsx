import StoryGenerator from "../components/StoryGenerator";

export default function Home() {
  return (
    <div className="app-container">
      <header>
        <h1>Interactive Story Generator</h1>
      </header>
      <main>
        <StoryGenerator />
      </main>
    </div>
  );
}
