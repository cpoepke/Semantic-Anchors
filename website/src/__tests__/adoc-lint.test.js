import { describe, it, expect } from 'vitest'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const anchorsDir = path.join(__dirname, '..', '..', '..', 'docs', 'anchors')

describe('AsciiDoc anchor content validation', () => {
  it('should not use Markdown-style numbered lists (1. 2. 3.) in .adoc files', () => {
    const files = fs.readdirSync(anchorsDir).filter((f) => f.endsWith('.adoc'))
    const violations = []

    for (const file of files) {
      const content = fs.readFileSync(path.join(anchorsDir, file), 'utf-8')
      const lines = content.split('\n')

      let inCodeBlock = false
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        // Track AsciiDoc code blocks (---- or ....)
        if (/^(-{4,}|\.{4,})$/.test(line.trim())) {
          inCodeBlock = !inCodeBlock
          continue
        }
        if (inCodeBlock) continue
        // Match lines starting with "1." "2." etc. (Markdown ordered list)
        if (/^\d+\.\s/.test(line)) {
          violations.push(`${file}:${i + 1}: "${line.trim()}"`)
        }
      }
    }

    expect(
      violations,
      `Found Markdown-style numbered lists in AsciiDoc files. ` +
        `Use AsciiDoc ordered list syntax (. item) instead:\n${violations.join('\n')}`
    ).toEqual([])
  })
})
