export default function PastRunsTable({ runs }) {
    const handleReplay = (filePath) => {
        const replayUrl = `/replay.html?url=${encodeURIComponent(filePath)}`;
        window.open(replayUrl, '_blank', 'width=1200,height=800');
    };

    return (
        <div className="mt-6 bg-white rounded shadow p-4">
            <h2 className="text-xl font-semibold mb-2">Past Runs</h2>
            <table className="w-full border-collapse">
                <thead>
                <tr className="bg-gray-100">
                    <th className="border p-2">DAG</th>
                    <th className="border p-2">Status</th>
                    <th className="border p-2">File</th>
                    <th className="border p-2">Actions</th>
                </tr>
                </thead>
                <tbody>
                {runs.map(run => (
                    <tr key={run.id} className="hover:bg-gray-50">
                        <td className="border p-2">{run.workflow}</td>
                        <td className="border p-2">{run.status}</td>
                        <td className="border p-2">
                            <a href={run.file_path} className="text-blue-600 underline" download>
                                {run.stored_filename}
                            </a>
                        </td>
                        <td className="border p-2">
                            <button
                                onClick={() => handleReplay(run.file_path)}
                                className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                            >
                                Replay
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
