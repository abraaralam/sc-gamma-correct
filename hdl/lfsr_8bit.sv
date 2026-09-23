`timescale 1ns / 1ps
// Galois implementation of LFSR

module lfsr_8bit (
  input  logic       clk,
  input  logic       rst_n,      
  output logic [7:0] lfsr_out
);

  logic [3:0] R1;
  logic       R2; 
  logic       R3; 
  logic [1:0] R4; 
  
  logic feedback;
  assign feedback = R1[3];
  assign lfsr_out = {R1, R2, R3, R4};

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      R1 <= 4'b0000;
      R2 <= 1'b0;
      R3 <= 1'b0;
      R4 <= 2'b01; // seed
    end else begin
      R4 <= {R4[0], feedback};
      R3 <= R4[1] ^ feedback;
      R2 <= R3 ^ feedback;
      R1 <= {R1[2:0], R2 ^ feedback};
    end
  end

endmodule