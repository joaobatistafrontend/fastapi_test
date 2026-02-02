import { useState } from "react";
import AtividadeForm from "../components/AtividadeForm";
import AtividadeList from "../components/AtividadeList";

export default function Home() {
  const [reload, setReload] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-6">
        <AtividadeForm onSuccess={() => setReload(!reload)} />
        <AtividadeList reload={reload} />
      </div>
    </div>
  );
}
