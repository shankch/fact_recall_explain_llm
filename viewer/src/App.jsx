import { useEffect, useMemo, useState } from "react";

function normalize(values) {
  const max = Math.max(...values, 1);
  return values.map((value) => value / max);
}

function ArchitecturePanel({ architecture, profile }) {
  if (!architecture || !profile) return null;
  const attn = normalize(profile.layer_attention_norms || []);
  const mlp = normalize(profile.layer_mlp_mean_abs || []);

  return (
    <section className="panel architecture-panel">
      <div className="panel-header">
        <h2>Gemma-3-270M-IT Architecture</h2>
        <p>{architecture.layers} decoder layers, {architecture.attention_heads} heads, hidden {architecture.hidden_size}</p>
      </div>
      <div className="architecture-grid">
        {(profile.layer_hidden_norms || []).map((value, index) => (
          <div className="layer-card" key={index}>
            <div className="layer-label">Layer {index}</div>
            <div className="component-track">
              <div
                className="component-box attention-box"
                style={{ opacity: 0.2 + (attn[index] || 0) * 0.8 }}
                title={`Attention norm ${value}`}
              >
                Attn
              </div>
              <div
                className="component-box mlp-box"
                style={{ opacity: 0.2 + (mlp[index] || 0) * 0.8 }}
                title={`MLP activity ${(profile.layer_mlp_mean_abs || [])[index] || 0}`}
              >
                MLP
              </div>
            </div>
            <div className="layer-metric">{value.toFixed(2)}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

function TopNeuronTable({ profile }) {
  if (!profile) return null;
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Top Lit-Up Neurons</h2>
        <p>Highest absolute MLP activations for this prompt</p>
      </div>
      <div className="top-neurons">
        {(profile.top_neurons || []).slice(0, 18).map((item, index) => (
          <div className="neuron-chip" key={`${item.layer}-${item.neuron}-${index}`}>
            <strong>L{item.layer}</strong>
            <span>N{item.neuron}</span>
            <em>{item.activation.toFixed(3)}</em>
          </div>
        ))}
      </div>
    </section>
  );
}

function PromptInspector({ profile, architecture }) {
  if (!profile) return null;
  return (
    <section className="panel inspector-panel">
      <div className="panel-header">
        <h2>Prompt Result</h2>
        <p>{profile.country || "Live prompt"} · expected {profile.expected_capital}</p>
      </div>
      <div className="inspector-grid">
        <div>
          <div className="label">Prompt</div>
          <div className="value-block">{profile.prompt}</div>
        </div>
        <div>
          <div className="label">Top prediction</div>
          <div className="value-block">{profile.top_prediction || "-"}</div>
        </div>
        <div>
          <div className="label">Generated continuation</div>
          <div className="value-block">{profile.generated_text || "-"}</div>
        </div>
        <div className="stats-row">
          <div className="stat-card">
            <span>Rank</span>
            <strong>{profile.target_rank}</strong>
          </div>
          <div className="stat-card">
            <span>Margin</span>
            <strong>{Number(profile.target_margin || 0).toFixed(3)}</strong>
          </div>
          <div className="stat-card">
            <span>Exact</span>
            <strong>{Number(profile.exact_match || 0).toFixed(2)}</strong>
          </div>
        </div>
        <div className="runtime-row">
          <div className="runtime-pill">
            <span>Device</span>
            <strong>{profile.device || architecture?.device || "unknown"}</strong>
          </div>
          <div className="runtime-pill">
            <span>DType</span>
            <strong>{profile.dtype || architecture?.dtype || "unknown"}</strong>
          </div>
          <div className="runtime-pill">
            <span>Latency</span>
            <strong>{profile.inference_ms ? `${profile.inference_ms} ms` : "-"}</strong>
          </div>
          <div className="runtime-pill">
            <span>GPU</span>
            <strong>{profile.gpu_name || (architecture?.device === "cuda" ? "CUDA device" : "CPU / fallback")}</strong>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function App() {
  const [architecture, setArchitecture] = useState(null);
  const [summary, setSummary] = useState(null);
  const [profiles, setProfiles] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState("");
  const [customPrompt, setCustomPrompt] = useState("What is the capital of India?");
  const [customCapital, setCustomCapital] = useState("New Delhi");
  const [liveProfile, setLiveProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch("/api/architecture").then((response) => response.json()),
      fetch("/api/capital-summary").then((response) => response.json()),
      fetch("/api/capital-prompts").then((response) => response.json())
    ]).then(([architectureData, summaryData, profilesData]) => {
      setArchitecture(architectureData);
      setSummary(summaryData);
      setProfiles(profilesData);
      if (profilesData.length) {
        setSelectedPrompt(profilesData[0].prompt);
      }
    });
  }, []);

  const selectedProfile = useMemo(
    () => profiles.find((profile) => profile.prompt === selectedPrompt) || liveProfile,
    [profiles, selectedPrompt, liveProfile]
  );

  async function analyzePrompt() {
    setLoading(true);
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: customPrompt, expected_capital: customCapital })
    });
    const data = await response.json();
    setLiveProfile(data);
    setSelectedPrompt("");
    setLoading(false);
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Mechanistic interpretability lab</p>
          <h1>Capital Prompt Activation Viewer</h1>
          <p className="hero-copy">
            Explore how Gemma-3-270M-IT reacts to capital-city prompts, which layers light up,
            and which MLP neurons activate most strongly for a given question.
          </p>
        </div>
        <div className="hero-stats">
          <div className="hero-stat">
            <span>Prompts</span>
            <strong>{summary?.num_prompts ?? "-"}</strong>
          </div>
          <div className="hero-stat">
            <span>Mean exact</span>
            <strong>{summary ? Number(summary.mean_exact_match).toFixed(3) : "-"}</strong>
          </div>
        <div className="hero-stat">
          <span>Shared layer</span>
          <strong>{summary?.strongest_shared_layer ?? "-"}</strong>
        </div>
        <div className="hero-stat">
          <span>Runtime</span>
          <strong>{architecture?.device || "-"}</strong>
        </div>
      </div>
      </header>

      <section className="controls">
        <div className="panel control-panel">
          <div className="panel-header">
            <h2>Precomputed Prompt</h2>
            <p>Browse one of the 100 capital prompts from the study</p>
          </div>
          <select value={selectedPrompt} onChange={(event) => { setSelectedPrompt(event.target.value); setLiveProfile(null); }}>
            {profiles.map((profile) => (
              <option key={profile.prompt} value={profile.prompt}>
                {profile.prompt}
              </option>
            ))}
          </select>
        </div>

        <div className="panel control-panel">
          <div className="panel-header">
            <h2>Live Prompt</h2>
            <p>Run a new prompt through the local API on the loaded model device</p>
          </div>
          <input value={customPrompt} onChange={(event) => setCustomPrompt(event.target.value)} />
          <input value={customCapital} onChange={(event) => setCustomCapital(event.target.value)} />
          <button onClick={analyzePrompt} disabled={loading}>{loading ? "Analyzing..." : "Analyze Prompt"}</button>
        </div>
      </section>

      <PromptInspector profile={selectedProfile} architecture={architecture} />
      <ArchitecturePanel architecture={architecture} profile={selectedProfile} />
      <TopNeuronTable profile={selectedProfile} />

      <section className="panel gallery-panel">
        <div className="panel-header">
          <h2>Study Heatmaps</h2>
          <p>Precomputed over 100 country-capital prompts</p>
        </div>
        <div className="gallery-grid">
          <figure>
            <img src="/artifacts/results/capital_study/capital_prompt_neuron_heatmap.png" alt="Neuron heatmap" />
            <figcaption>Prompt × top-neuron activation heatmap</figcaption>
          </figure>
          <figure>
            <img src="/artifacts/results/capital_study/capital_layer_hidden_heatmap.png" alt="Layer heatmap" />
            <figcaption>Prompt × layer hidden-state norm heatmap</figcaption>
          </figure>
          <figure>
            <img src="/artifacts/results/capital_study/capital_architecture_component_profile.png" alt="Component profile" />
            <figcaption>Average architecture component profile</figcaption>
          </figure>
        </div>
      </section>
    </main>
  );
}
