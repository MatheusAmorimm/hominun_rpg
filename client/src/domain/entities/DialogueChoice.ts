export interface DialogueChoice {
  id: string;
  text: string;
  requires_flag?: string;
  leads_to?: string;
}

export interface DialogueNode {
  id: string;
  speaker: string;
  text: string;
  choices: DialogueChoice[];
}
