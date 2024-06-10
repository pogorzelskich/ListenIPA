import torch
import torch.nn as nn
from torch import complex64


class ListenIPA(nn.Module):
    def __init__(self, audio_input_size, criteria_len, kernel_size, num_layers, is_var1):
        super(ListenIPA, self).__init__()
        self.audio_input_size = audio_input_size
        self.criteria_len = criteria_len
        self.new_hidden_size = 129
        self.kernel_size = kernel_size
        self.num_layers = num_layers
        self.is_var1 = is_var1

        if is_var1:
            self.conv1 = nn.Conv1d(1, 1, kernel_size=kernel_size, stride=kernel_size//7,
                                   padding=kernel_size//2, dtype=complex64, bias=False)
        else:
            self.conv1 = nn.Conv1d(1, 1, kernel_size=kernel_size, stride=kernel_size//7,
                                   padding=kernel_size//2, dtype=complex64, bias=True)
        
        self.conv2 = nn.Conv1d(1, 1, kernel_size=kernel_size, stride=kernel_size//7,
                               padding=kernel_size//2, dtype=complex64, bias=False)

        self.initial_linears2 = nn.Sequential(
            nn.Linear(self.new_hidden_size * 2, self.new_hidden_size, bias=False),
            nn.Linear(self.new_hidden_size, self.new_hidden_size, bias=False),
        )

        if is_var1:
            self.recc = nn.LSTM(self.new_hidden_size, self.new_hidden_size, num_layers, batch_first=False)
        else:
            self.recc = nn.GRU(self.new_hidden_size, self.new_hidden_size, num_layers, batch_first=False)

        self.final_linears1 = nn.Sequential(
            nn.Linear(self.new_hidden_size, criteria_len, bias=False),
        )

    def forward(self, x, hidden):
        x = self.conv1(x)
        x = self.conv2(x)
        x = torch.cat((x.real, x.imag), dim=-1)
        x = self.initial_linears2(x)
        x, hidden = self.recc(x, hidden)
        x = self.final_linears1(x)
        return x, hidden

    def init_hidden(self):
        if self.is_var1:
            return (torch.zeros(self.num_layers, 1, self.new_hidden_size),
                    torch.zeros(self.num_layers, 1, self.new_hidden_size))
        else:
            return torch.zeros(self.num_layers, 1, self.new_hidden_size)