export const dynamic = "force-dynamic";

let clients: any[] = []

export async function POST(request: Request) {
    const data = await request.json()
    console.log("Received data from webhook:", data)

    console.log(clients)
    // sends to all clients instead of the specific one the project belongs to.
    clients.forEach(c => {
        try {
            console.log("Sending data to client", c.id)
            c.controller.enqueue(new TextEncoder().encode(`data: ${JSON.stringify(data)}\n\n`))
        } catch (e) {
            console.error(`Error sending data to client ${c.id}`, e)
            clients = clients.filter(cl => c.id !== cl.id)
        }
    })
    return new Response("Data received", {status: 200})

}

export async function GET() {
    const encoder = new TextEncoder()
    const clientId = crypto.randomUUID()

    const customReadable = new ReadableStream({
        start(controller) {
            clients.push({id: clientId, controller})
            controller.enqueue(encoder.encode(`data: ${JSON.stringify({type: 'connected'})}\n\n`))
        },
        cancel() {
            clients = clients.filter(c => c.id !== clientId);
            console.log(`Client ${clientId} disconnected. total clients: ${clients.length}`)
        }
    })
    return new Response(customReadable, {
        headers: {
            Connection: "keep-alive",
            "Cache-Control": "no-cache, no-transform",
            "Content-Type": "text/event-stream; charset=utf-8",
        },
    })
}