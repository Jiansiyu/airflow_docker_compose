export default function FileUploadForm({ onUpload, categories, workflows }) {
    return (
        <div className="space-y-4 border p-4 rounded shadow bg-white">
            <input
                type="file"
                onChange={e => onUpload.setFile(e.target.files[0])}
                className="block w-full border border-gray-300 p-2 rounded"
            />
            <div className="flex space-x-4">
                <select
                    value={onUpload.category}
                    onChange={e => onUpload.setCategory(e.target.value)}
                    className="flex-1 border border-gray-300 p-2 rounded"
                >
                    <option value="">Select category</option>
                    {categories.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                    ))}
                </select>
                <select
                    value={onUpload.workflow}
                    onChange={e => onUpload.setWorkflow(e.target.value)}
                    className="flex-1 border border-gray-300 p-2 rounded"
                >
                    <option value="">Select workflow</option>
                    {workflows.map(wf => (
                        <option key={wf} value={wf}>{wf}</option>
                    ))}
                </select>
            </div>
            <button
                onClick={onUpload.uploadAndStart}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                Start
            </button>
        </div>
    );
}
