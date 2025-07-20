import StoryLoader from "../../../components/StoryLoader";

export default function StoryPage({ params }: { params: { id: string } }) {
  return (
    <div className="app-container">
      <header>
        <h1>Interactive Story Generator</h1>
      </header>
      <main>
        <StoryLoader id={parseInt(params.id)} />
      </main>
    </div>
  );
} 